import os
import json
import sys
import logging
from vconnector.vertica_connector import VerticaConnector
# from user import user


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.captureWarnings(True)

SCHEMA = "netology_mart"
STAGING_SCHEMA = "netology_staging"
TABLE_NAME = "carts_and_orders_short" #os.getenv("table_name")

SQL_C1 ="""
/* Без отдельных выплат по рассрочкам 1 часть. Продукты*/
CREATE LOCAL TEMPORARY TABLE temp_carts_prep ON COMMIT PRESERVE ROWS AS
	SELECT ci.id::integer                                         AS cart_item_id,
           ci.resource_type::varchar(50),
           ci.resource_id::integer,
           ci.student_id::integer,
           ci.source_price::float,
           ci.price::float,
           CASE WHEN c.state = 'success' THEN ci.price::float END AS paid_amount,
           ci.cart_id::integer,
           ci.created_at::timestamp,
           'cart_items'::varchar(25)                              AS from_table,
           ci.id::integer                                         AS from_table_id,
           c.tags                                                 AS tags,
           CASE WHEN regexp_like(tags, 'b2c2b') THEN 1 ELSE 0 END AS b2c2b
    FROM netology_mysql.cart_items ci
            JOIN netology_mysql.carts c ON ci.cart_id = c.id
    WHERE resource_type NOT IN ('InstallmentPart', 'Moving', 'Products::AdditionalBlock')
UNSEGMENTED ALL NODES;
"""

SQL_C2 = """
/* 2 часть. Рассрочки - все данные сводим к первому заказу */
INSERT INTO temp_carts_prep
    SELECT f.cart_item_id  AS                                  cart_item_id, -- первый cart_item для рассрочки
           i.resource_type,
           i.resource_id,
           ci.student_id   AS                                  student_id,
           i.source_amount AS                                  source_price,
           i.amount        AS                                  price,
           CASE WHEN i.paid_amount != 0 THEN i.paid_amount END paid_amount,  --чтобы соответсвовало логике продуктов, иначе вместо NULL будет 0
           f.cart_id       AS                                  cart_id,      -- первый cart для рассрочки
           ci.created_at,
           'installments'  AS                                  from_table,
           i.id            AS                                  from_table_id,
           carts.tags      AS                                  tags,
           CASE WHEN regexp_like(tags, 'b2c2b') THEN 1 ELSE 0 END AS b2c2b
    FROM netology_mysql.installments i
             JOIN (
        /* Первый заказ по рассрочке
         Есть ли в рассрочке не отмененные корзины?
         если есть, то берем первую не fail*/
        SELECT i.id,
               MIN(ci.id)      AS cart_item_id,
               MIN(ci.cart_id) AS cart_id
        FROM netology_mysql.cart_items ci
                 JOIN netology_mysql.installment_parts ip
                      ON ci.resource_id = ip.id AND ci.resource_type = 'InstallmentPart'
                 JOIN netology_mysql.installments i ON ip.installment_id = i.id
                 JOIN netology_mysql.carts ON carts.id = ci.cart_id
        WHERE ci.resource_type = 'InstallmentPart'
          AND ip.state != 'removed'
          AND carts.state != 'fail'
        GROUP BY i.id
        UNION ALL
        /* если нет, то просто первую (not_failed = 0)*/
        SELECT i.id,
               MIN(ci.id)      AS cart_item_id,
               MIN(ci.cart_id) AS cart_id
        FROM netology_mysql.cart_items ci
                 JOIN netology_mysql.installment_parts ip
                      ON ci.resource_id = ip.id AND ci.resource_type = 'InstallmentPart'
                 JOIN netology_mysql.installments i ON ip.installment_id = i.id
                 JOIN netology_mysql.carts ON carts.id = ci.cart_id
        WHERE ci.resource_type = 'InstallmentPart'
          AND ip.state != 'removed'
          AND i.id IN (
            SELECT id
            FROM (SELECT i.id,
                         SUM(CASE WHEN carts.state != 'fail' THEN 1 ELSE 0 END) AS not_failed
                  FROM netology_mysql.cart_items ci
                           JOIN netology_mysql.installment_parts ip ON ci.resource_id = ip.id AND
                                                                       ci.resource_type = 'InstallmentPart'
                           JOIN netology_mysql.installments i ON ip.installment_id = i.id
                           JOIN netology_mysql.carts ON carts.id = ci.cart_id
                  WHERE ci.resource_type = 'InstallmentPart'
                    AND ip.state != 'removed'
                  GROUP BY i.id
                 ) t
            WHERE not_failed = 0
        )
        GROUP BY i.id
    ) AS f ON i.id = f.id
             JOIN netology_mysql.cart_items ci ON f.cart_item_id = ci.id
             JOIN netology_mysql.carts ON ci.cart_id = carts.id
;
"""

SQL_C3 = """
/* 3 часть. Доплаты при переносах*/
INSERT INTO temp_carts_prep
    SELECT ci.id                                          AS cart_item_id,
           m.to_resource_type                             AS resource_type,
           m.to_resource_id                               AS resource_id,
           ci.student_id                                  AS student_id,
           m.price                                        AS source_price,
           m.price,
           CASE WHEN m.state = 'success' THEN m.price END AS paid_amount,
           ci.cart_id                                     AS cart_id,
           ci.created_at,
           'movings'                                      AS from_table,
           m.id                                           AS from_table_id,
           NULL                                           AS tags,
           CASE WHEN regexp_like(tags, 'b2c2b') THEN 1 ELSE 0 END AS b2c2b
    FROM netology_mysql.movings m
             JOIN netology_mysql.cart_items ci ON m.id = ci.resource_id AND ci.resource_type = 'Moving'
             JOIN netology_mysql.carts c on ci.cart_id = c.id
;
"""

SQL_C4 = """
/* 4 часть. Дополнительные блоки*/
INSERT INTO temp_carts_prep
    SELECT ci.id                                           AS cart_item_id,
           'Legacy::Program'                               AS resource_type,
           pab.program_id                                  AS resource_id,
           ci.student_id                                   AS student_id,
           ci.source_price,
           ci.price,
           CASE WHEN c.state = 'success' THEN ci.price END AS paid_amount,
           ci.cart_id,
           ci.created_at,
           'product_additional_blocks'                     AS from_table,
           pab.id                                          AS from_table_id,
           NULL                                            AS tags,
           CASE WHEN regexp_like(tags, 'b2c2b') THEN 1 ELSE 0 END AS b2c2b
    FROM netology_mysql.cart_items ci
             JOIN netology_mysql.carts c ON ci.cart_id = c.id
             JOIN netology_mysql.product_additional_blocks pab
                  ON ci.resource_id = pab.id AND ci.resource_type = 'Products::AdditionalBlock'
    WHERE ci.resource_type = 'Products::AdditionalBlock'
;

SELECT ANALYZE_STATISTICS ('temp_carts_prep');
"""

SQL_C5 = """
/* Сбор данных по заказам - Часть 1. сбор всех данных */
CREATE LOCAL TEMPORARY TABLE temp_carts_0 ON COMMIT PRESERVE ROWS AS
	SELECT 'carts'::varchar(10)                                         AS carts_orders,
	       cia.cart_item_id                                         AS cart_items_id,
	       cia.cart_id                                              AS cart_id,
	       cia.resource_type,
	       cia.resource_id,
	       cia.student_id,
	       cia.source_price,                                                  -- цена, которая была на витрине
	       cia.price                                                AS price, -- цена с учетом скидки
	       cia.paid_amount,                                                   -- оплаченная сумма
	       cia.from_table,
	       cia.from_table_id,
	       carts.purchaser_id                                       AS purchaser_id,
	       --NULL ::varchar(10000)                                    AS purchaser_name,
	       --null ::int                                               AS purchaser_phone,
	       --NULL ::varchar(10000)                                    AS purchaser_email,
	       --null ::datetime	                                        AS purchaser_created_at,
	       cia.created_at                                           AS cart_items_created_at,
	       carts.created_at                                         AS carts_created_at,
	       carts.succeeded_at                                       AS carts_succeeded_at,
	       carts.state,
	       carts.state != 'fail'                                    AS _leads,
	       CASE
	           WHEN cia.from_table = 'installments' THEN 'part'
	           ELSE 'full'
	           END::VARCHAR                                         AS pay_type,
	       pc.code::VARCHAR                                         AS promo_code,
	       CASE WHEN carts.company_id IS NOT NULL THEN 1 ELSE 0 END AS purchaser_as_company,
	       cns.manager_id                                           AS manager_id,
	       --null::varchar(10000)                                     AS manager_name,
	       cia.tags::varchar(10000)                                 AS tags,
	       cia.b2c2b,
           cla_sgmt.segmet_ABC                                      AS segment_ABC
	       /*
	       ,
	       case
           when tsd_cart.channel = 'cpc' then
               case
                   when tsd_cart.utm_source in
                        ('fb', 'vk', 'dzen', 'tiktok', 'facebook', 'mt', 'fb_wh', 'twitter', 'vc', 'linkedin',
                         'mytarget', 'instagram','vkontakte','vkads') or 
                        ((tsd_cart.utm_campaign='brand_all_bou_tg_target_db_chatbot' or
                          tsd_cart.utm_campaign='brand_all_bou_tg_target_db_chatbot_atlas')
                         and tsd_cart.utm_source = 'tg')
                   then 'cpc_target'
                   else 'cpc_context' end
           else tsd_cart.channel end                                as channel,
	       tsd_cart.utm_campaign                                    AS "utm_campaign",
	       tsd_cart.utm_source                                      AS "utm_source",
	       tsd_cart.utm_medium                                      AS "utm_medium",
	       tsd_cart.utm_content                                     AS "utm_content",
	       tsd_cart.utm_term                                        AS "utm_term",
	       tsd_cart.referrer                                        AS "referrer"
	       */
	FROM temp_carts_prep cia
	         JOIN netology_mysql.carts ON cia.cart_id = carts.id
	         LEFT JOIN netology_mysql.promo_codes pc ON carts.promo_code_id = pc.id
--	         LEFT JOIN netology_mart.user_main_phones phone ON carts.purchaser_id = phone.user_id
	         LEFT JOIN (
                            SELECT cart_id
                                   , manager_id
                            FROM netology_mysql.consultations
                            WHERE consultations.manager_id IS NOT NULL
                            GROUP BY cart_id
                                   , manager_id
                            )cns
	                   ON cns.cart_id = cia.cart_id AND
	                      cia.from_table NOT IN ('movings', 'product_additional_blocks')
--	         LEFT JOIN netology_mysql.users u ON carts.purchaser_id = u.id
--	         LEFT JOIN netology_mysql.traqtor_source_data tsd_cart
--	                   ON tsd_cart.resource_id = cia.cart_id
--	                       AND tsd_cart.resource_type = 'Cart'
	         LEFT JOIN (SELECT cla.name,
	                           cart_id,
	                           value AS segmet_ABC,
	                           created_at,
	                           ROW_NUMBER() OVER(partition by cart_id ORDER BY created_at DESC) as num
	                    FROM netology_mysql.cart_lead_attributes cla
	                    WHERE 1 = 1
	                      AND cla.name = 'СЕГМЕНТ А В С') cla_sgmt ON cla_sgmt.cart_id = cia.cart_id and num=1
--WHERE cia.cart_id = 752694
UNSEGMENTED ALL NODES;
SELECT ANALYZE_STATISTICS ('temp_carts_0')
;
"""

SQL_C5_1 = """
/* Сбор данных по заказам - Часть 1.1. Добавление данных из тарктора */

CREATE LOCAL TEMPORARY TABLE temp_carts_0_tr ON COMMIT PRESERVE ROWS AS
select c.* ,
    	       case
           when tsd_cart.channel = 'cpc' then
               case
                   when tsd_cart.utm_source in
                        ('fb', 'vk', 'dzen', 'tiktok', 'facebook', 'mt', 'fb_wh', 'twitter', 'vc', 'linkedin',
                         'mytarget', 'instagram','vkontakte','vkads')  or 
                        ((tsd_cart.utm_campaign='brand_all_bou_tg_target_db_chatbot' or
                          tsd_cart.utm_campaign='brand_all_bou_tg_target_db_chatbot_atlas')
                         and tsd_cart.utm_source = 'tg')
                   then 'cpc_target'
                   else 'cpc_context' end
           else tsd_cart.channel end                                as channel,
	       tsd_cart.utm_campaign                                    AS "utm_campaign",
	       tsd_cart.utm_source                                      AS "utm_source",
	       tsd_cart.utm_medium                                      AS "utm_medium",
	       tsd_cart.utm_content                                     AS "utm_content",
	       tsd_cart.utm_term                                        AS "utm_term",
	       tsd_cart.referrer                                        AS "referrer"
from temp_carts_0 c
LEFT JOIN netology_mysql.traqtor_source_data tsd_cart --temp_traqtor_source
    ON tsd_cart.resource_id = c.cart_id
    AND tsd_cart.resource_type = 'Cart'
UNSEGMENTED ALL NODES;
SELECT ANALYZE_STATISTICS ('temp_carts_0_tr')
;
"""

SQL_C6 = """
/*Сбор данных по заказам - Часть 2. Подгружаем справочную инфу по клиентам и менеджерам*/

CREATE LOCAL TEMPORARY TABLE temp_carts ON COMMIT PRESERVE ROWS AS
	SELECT carts_orders,
	       c.cart_items_id,
	       c.cart_id,
	       c.resource_type,
	       c.resource_id,
	       c.student_id,
	       c.source_price,                                                  -- цена, которая была на витрине
	       c.price,															-- цена с учетом скидки
	       c.paid_amount,                                                   -- оплаченная сумма
	       c.from_table,
	       c.from_table_id,
	       c.purchaser_id,
	       u.name:: varchar(510)                                    AS purchaser_name,
	       phone.phone:: varchar(510)                               AS purchaser_phone,
	       u.email:: varchar(510)                     				AS purchaser_email,
	       u.created_at	                    	                    AS purchaser_created_at,
	       c.cart_items_created_at,
	       c.carts_created_at,
	       c.carts_succeeded_at,
	       c.state,
	       c._leads,
	       c.pay_type,
	       c.promo_code,
	       c.purchaser_as_company,
	       c.manager_id,
	       m.name 					                                AS manager_name,
	       c.tags,
	       c.b2c2b,
           c.segment_ABC,
	       c.channel,
	       c.utm_campaign,
	       c.utm_source,
	       c.utm_medium,
	       c.utm_content,
	       c.utm_term,
	       c.referrer
	FROM temp_carts_0_tr c
	         LEFT JOIN netology_mart.user_main_phones phone ON c.purchaser_id = phone.user_id
	      	 LEFT JOIN netology_mysql.users u ON c.purchaser_id = u.id
	         LEFT JOIN netology_mysql.users m ON c.manager_id = m.id
UNSEGMENTED ALL NODES;
SELECT ANALYZE_STATISTICS ('temp_carts')
;
"""

SQL_C7 = """
/* Сбор продаж и чистых продаж из оплат */

CREATE LOCAL TEMPORARY TABLE temp_carts_real_sales ON COMMIT PRESERVE ROWS AS
WITH payment_transactions AS (
			SELECT id AS pt_id,
					resource_id AS cart_id,
					payment_method,
					amount,
					real_amount_with_pennies / 100 AS real_amount,
					row_number() over(PARTITION BY resource_id ORDER BY id) AS rn
			FROM netology_mysql.payment_transactions
			WHERE 1=1
					AND resource_type = 'Cart' -- для заказов
					AND transaction_type = 'payment' -- только оплаты
					AND state = 'succeeded' -- успешные
	    ),
	real_amounts AS ( 
			SELECT q.cart_items_id,
				   sum(case
							when t.payment_method in ('tinkoff_installment', 'sberbank_installment', 'pos_credit_installment') 
		         				then (t.real_amount * (q.price / t.amount)) -- по кредитным оплатам сумма транзакции пропорционально вкладу каждого item в цену корзины
				         	else q.paid_amount
				        end) as real_sales_amount -- чистые продажи 
			FROM temp_carts as q 
			-- одна успешная транзакция по оплате заказа
			LEFT JOIN payment_transactions as t ON t.cart_id = q.cart_id
											   AND t.rn = 1 
											   AND q.carts_orders = 'carts'
			WHERE q.from_table != 'installments' 
				  AND q.paid_amount > 0
			group by q.cart_items_id
	    ),
	real_amounts_installments as (
			SELECT c.id as cart_id,
				   ip.installment_id,
                   sum(case
				   		 when t.payment_method in ('tinkoff_installment', 'sberbank_installment', 'pos_credit_installment')
				   			then t.real_amount
				   		 else greatest(ip.price, 0)
				   	   end) over(partition by ip.installment_id) as real_sales_amount -- чистые продажи
			FROM netology_mysql.installment_parts as ip
			JOIN netology_mysql.cart_items as ci ON ip.id = ci.resource_id
							                 	AND ci.resource_type = 'InstallmentPart'
			JOIN netology_mysql.carts as c ON ci.cart_id = c.id
                                            AND c.state = 'success'
			-- первая успешная транзакция по оплате заказа
			LEFT JOIN payment_transactions as t ON t.cart_id = c.id
												AND t.rn = 1
			WHERE ip.state = 'success'
	    )
SELECT carts_orders,
        c.cart_items_id,
        c.cart_id,
        c.resource_type,
        c.resource_id,
        c.student_id,
        c.source_price,                                                  			    -- цена, которая была на витрине
        c.price,																		-- цена с учетом скидки
        (
            least(coalesce( case
                                when c.state = 'success'
                                    and c.paid_amount = 0
                                    and ra.real_sales_amount is null then 0
                                when c.state = 'success' then ra.real_sales_amount end,
                            case when rai.real_sales_amount != 0
                                    then rai.real_sales_amount end), c.paid_amount)
            / greatest(c.paid_amount, 1) * c.price
        )::numeric(11, 2) as real_price,                                                -- цена исходя из чистых продаж
        c.paid_amount,                                                   			    -- оплаченная сумма
        coalesce(case
                    when c.state = 'success'
                        and c.paid_amount = 0
                        and ra.real_sales_amount is null then 0
                    when c.state = 'success' then ra.real_sales_amount end,
                case when rai.real_sales_amount != 0
                        then rai.real_sales_amount end) as real_amount,	        -- чистые продажи
        c.from_table,
        c.from_table_id,
        c.purchaser_id,
        c.purchaser_name,
        c.purchaser_phone,
        c.purchaser_email,
        c.purchaser_created_at,
        c.cart_items_created_at,
        c.carts_created_at,
        c.carts_succeeded_at,
        c.state,
        c._leads,
        c.pay_type,
        c.promo_code,
        c.purchaser_as_company,
        c.manager_id,
        c.manager_name,
        c.tags,
        c.b2c2b::BOOLEAN as b2c2b,
        c.segment_ABC,
        c.channel,
        c.utm_campaign,
        c.utm_source,
        c.utm_medium,
        c.utm_content,
        c.utm_term,
        c.referrer
FROM temp_carts c
-- первая успешная транзакция по оплате заказа
LEFT JOIN real_amounts AS ra ON ra.cart_items_id = c.cart_items_id
							AND c.from_table != 'installments'
-- первая успешная транзакция по оплате заказа installments
LEFT JOIN real_amounts_installments AS rai ON rai.cart_id = c.cart_id
										  AND c.from_table = 'installments'
UNSEGMENTED ALL NODES;
SELECT ANALYZE_STATISTICS ('temp_carts_real_sales')
;
"""

SQL_C8 = """
/* Сбор данных по заявкам */
CREATE LOCAL TEMPORARY TABLE temp_orders ON COMMIT PRESERVE ROWS AS
SELECT 'orders'                                                   AS carts_orders,
           o_new.orders_id                                        AS cart_items_id,
           o_new.orders_id                                        AS cart_id,
           'Legacy::Program'                                      AS resource_type,
           o_new.orders_program_id                                AS resource_id,
           o_new.orders_user_id                                   AS student_id,
           o_new._cash_price                                      AS source_price,
           o_new._cash_price                                      AS price,
           o_new._cash_price                                      AS real_price,
           o_new._cash_price                                      AS paid_amount,
           o_new._cash_price                                      AS real_amount,
           'orders_new'                                           AS from_table,
           o_new.orders_id                                        AS from_table_id,
           o_new.orders_user_id                                   AS purchaser_id,
           o_new.orders_name									  AS purchaser_name,
           o_new.orders_phone                                     AS purchaser_phone,
           o_new.orders_email                                     AS purchaser_email,
           u.created_at                                           AS purchaser_created_at,
           o_new.orders_add_date::TIMESTAMP - INTERVAL '3 hours'  AS cart_items_created_at,
           o_new.orders_add_date::TIMESTAMP - INTERVAL '3 hours'  AS carts_created_at,
           o_new.orders_pay_date::TIMESTAMP - INTERVAL '3 hours'  AS carts_succeeded_at,
           case
                    when o_new._cash_price is not null then 'success'
                    when o_new.orders_status in (6, 8, 11, 16, 18) then 'fail'
                    else 'pending' end                            AS state,
           o_new._leads                                           AS _leads,
           o_new._payment_type::VARCHAR                           AS pay_type,
           o_new.bonus_code::VARCHAR	            			  AS promo_code,
           CASE WHEN o_new.orders_face_type = 1 THEN 0 ELSE 1 END AS purchaser_as_company,
           o_new.orders_manager_id							      AS manager_id,
           NULL                                                   AS manager_name, /*забиваем в старых заявках, чтобы не утяжелять запрос*/
           NULL                                                   AS tags, /*забиваем в старых заявках на теги*/
           NULL::BOOLEAN                                          AS b2c2b,
           NULL                                                   AS segment_ABC,
           case
           when tsd_order.channel = 'cpc' then
               case
                   when tsd_order.utm_source in
                        ('fb', 'vk', 'dzen', 'tiktok', 'facebook', 'mt', 'fb_wh', 'twitter', 'vc', 'linkedin',
                         'mytarget', 'instagram','vkontakte','vkads')   or 
                        ((tsd_order.utm_campaign='brand_all_bou_tg_target_db_chatbot' or
                          tsd_order.utm_campaign='brand_all_bou_tg_target_db_chatbot_atlas')
                         and tsd_order.utm_source = 'tg')
                   then 'cpc_target'
                   else 'cpc_context' end
           else tsd_order.channel end                                       AS "channel",
           tsd_order.utm_campaign                                 AS "utm_campaign",
           tsd_order.utm_source                                   AS "utm_source",
           tsd_order.utm_medium                                   AS "utm_medium",
           tsd_order.utm_content                                  AS "utm_content",
           tsd_order.utm_term                                     AS "utm_term",
           tsd_order.referrer                                     AS "referrer"
    FROM netology_mart.orders_new o_new
             JOIN netology_mysql.orders o ON o_new.orders_id = o.id
             LEFT JOIN netology_mysql.traqtor_source_data tsd_order
                       ON tsd_order.resource_id = o_new.orders_id
                           AND tsd_order.resource_type = 'Legacy::Order'
             LEFT JOIN netology_mysql.users u on o.user_id = u.id
    WHERE TRUE
      AND o_new.orders_id = o_new._parent_order_id_2 -- заявки первого уровня
      AND o_new.orders_in_profession = 0             -- не аккредитации в рамках профессии
      AND o.archive = 0 -- не архивные
      AND o_new.orders_id not in (select order_id from netology_mysql.order_to_carts) -- искл orders которые мигрировали в систему carts
UNSEGMENTED ALL NODES;
SELECT ANALYZE_STATISTICS ('temp_orders')
;
"""

SQL = """
    SELECT c.carts_orders,
       c.cart_items_id,
       c.cart_id,
       c.resource_type,
       c.resource_id,
       c.student_id,
       c.source_price,
       c.price,
       c.real_price,
       c.paid_amount,
       c.real_amount,
       c.from_table,
       c.from_table_id,
       c.purchaser_id,
       c.purchaser_name,
       c.purchaser_phone,
       c.purchaser_email,
       c.purchaser_created_at,
       c.cart_items_created_at,
       c.carts_created_at,
       c.carts_succeeded_at,
       c.state,
       c._leads,
       c.pay_type,
       c.promo_code,
       c.purchaser_as_company,
       c.manager_id,
       c.manager_name,
       c.tags,
       c.b2c2b,
       c.segment_ABC,
       c.channel,
       c.utm_campaign,
       c.utm_source,
       c.utm_medium,
       c.utm_content,
       c.utm_term,
       c.referrer
FROM temp_carts_real_sales c
UNION ALL
SELECT o.carts_orders,
       o.cart_items_id,
       o.cart_id,
       o.resource_type,
       o.resource_id,
       o.student_id,
       o.source_price,
       o.price,
       o.real_price,
       o.paid_amount,
       o.real_amount,
       o.from_table,
       o.from_table_id,
       o.purchaser_id,
       o.purchaser_name,
       o.purchaser_phone,
       o.purchaser_email,
       o.purchaser_created_at,
       o.cart_items_created_at,
       o.carts_created_at,
       o.carts_succeeded_at,
       o.state,
       o._leads,
       o.pay_type,
       o.promo_code,
       o.purchaser_as_company,
       o.manager_id,
       o.manager_name,
       o.tags,
       o.b2c2b,
       o.segment_ABC,
       o.channel,
       o.utm_campaign,
       o.utm_source,
       o.utm_medium,
       o.utm_content,
       o.utm_term,
       o.referrer
FROM temp_orders o
;
"""

SQL_D = """
DROP TABLE IF EXISTS temp_carts_prep;
DROP TABLE IF EXISTS temp_carts_0;
DROP TABLE IF EXISTS temp_carts_0_tr;
DROP TABLE IF EXISTS temp_carts;
DROP TABLE IF EXISTS temp_orders;
DROP TABLE IF EXISTS temp_carts_real_sales;
"""

def run():
    with VerticaConnector(
            user=os.getenv("VERTICA_WRITE_USER"),
            password=os.getenv("VERTICA_WRITE_PASSWORD"),
            database="DWH",
            vertica_configs=json.loads(os.getenv("VERTICA_CONFIGS")),
    ) as v_connector:
        cursor = v_connector.cnx.cursor()
        v_connector.create_staging_table(
            table_name=TABLE_NAME,
            schema=SCHEMA,
            staging_schema=STAGING_SCHEMA,
            ddl_path=os.path.dirname(os.path.dirname(__file__)) + "/db/vertica/" + SCHEMA
        )
        cursor.execute(SQL_D)
        for i in (SQL_C1, SQL_C2, SQL_C3, SQL_C4, SQL_C5, SQL_C5_1, SQL_C6, SQL_C7, SQL_C8):
            logging.info(i)
            cursor.execute(i)

        sql = "INSERT INTO {staging_schema}.{table_name} ".format(staging_schema=STAGING_SCHEMA,
                                                                  table_name=TABLE_NAME) + SQL
        logging.info(sql)
        cursor.execute(sql)
        v_connector.reload_main_table(
            table_name=TABLE_NAME,
            schema=SCHEMA,
            staging_schema=STAGING_SCHEMA
        )

        cursor.execute(SQL_D)


if __name__ == "__main__":
    run()
