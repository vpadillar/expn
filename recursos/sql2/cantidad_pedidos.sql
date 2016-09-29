select extract(year from current_date)
select * from pedido_configuraciontiempo where id=2

update pedido_configuraciontiempo set primero = 1 , segundo =30

select cast(''||extract(year from current_date)||'-'||6||'-'||30||'' as date)

select * from 