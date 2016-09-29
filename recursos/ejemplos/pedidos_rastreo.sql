select replace(t.direccion,'"','') as direccion,t.num_pedido 
from (select  id,(cast(cliente as json)::json->'direccion')::text as direccion,
case when num_pedido is null or length(num_pedido)=0 then 'pedido_Ws' else num_pedido end as num_pedido  from pedido_pedidows 
where motorizado_id=8 and entregado=false and activado=true and despachado=true
union
select p.id, c.direccion as direccion,case when p.num_pedido is not null then p.num_pedido else 'pedido_plataforma' end as num_pedido 
from pedido_pedido as p inner join usuario_cliente as c on(p.cliente_id=c.id and p.motorizado_id=8 and p.entregado=false)) as t


select * from pedido_pedido
select * from pedido_pedidows