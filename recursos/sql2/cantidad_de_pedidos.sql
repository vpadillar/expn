select * from public.pedido_pedido;
select * from public.auth_user

select segundo from public.pedido_configuraciontiempo

select * from pub
select cast(''||extract(year from current_date)||'-'||'12'||'-'||1 as date)
update public.pedido_configuraciontiempo set sugundo = 6 where id=2
select * from public.pedido_pedido as p inner join public.usuario_empresa as e on(e.id=p.empresa_id)

select * from public.pedido_pedido as p inner join public.pedido_configuraciontiempo as c on (p.empresa_id=c.empresa_id)
 where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=1 order by confi.id desc limit 1) and p.fecha_pedido
                between
                       case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
                               else
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                        end
                and
                        case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                                else
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)+1||'-'||c.primero as date)
                         end


 (select last(id) from public.pedido_configuraciontiempo as confi where confi.empresa_id=1 )
select extract(month from current_date)
select * from public.pedido_pedidows
select * from pedido_pedido
update pedido_pedido set entregado=true where id=21
select * from public.pedido_pedido as p inner join public.pedido_configuraciontiempo as c on (p.empresa_id=c.empresa_id and p.activado = true and p.entregado= true)
 where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=1 order by confi.id desc limit 1) and p.fecha_pedido
                between
                       case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
                               else
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                        end
                and
                        case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                                else
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)+1||'-'||c.primero as date)
                         end
select * from public.usuario_tienda
select * from public.pedido_pedidows as p inner join public.usuario_tienda as  inner join public.pedido_configuraciontiempo as c on (p.empresa_id=c.empresa_id and p.activado = true and p.entregado= true)
  where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=1 order by confi.id desc limit 1) and p.fecha_pedido
                 between
                        case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
                                else
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                         end
                 and
                         case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                              cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                                 else
                              cast(''||extract(year from current_date)||'-'||extract(month from current_date)+1||'-'||c.primero as date)
                          end
