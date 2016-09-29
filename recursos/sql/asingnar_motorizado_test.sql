CREATE OR REPLACE FUNCTION unit_test() RETURNS boolean AS

$$
declare
  test1 boolean;
  test2 boolean;
  test3 boolean;
begin
  test1 := (select auto_asignar(2, '[{"identificador":"3","lat": 10.390944, "lng": -75.478158},{"identificador":"1","lat": 10.391707, "lng": -75.479040}, {"identificador":"2","lat": 10.3790921, "lng": -75.4738238}]')) = '3';
  RAISE NOTICE 'La prueba 1 arrojo un %', test1;
  test2 := (select auto_asignar(2, '[{"identificador":"2","lat": 10.390944, "lng": -75.478158},{"identificador":"1","lat": 10.391707, "lng": -75.479040}, {"identificador":"3","lat": 10.3790921, "lng": -75.4738238}]')) = '2';
  RAISE NOTICE 'La prueba 2 arrojo un %', test2;
  test3 := (select auto_asignar(2, '[{"identificador":"3","lat": 10.390944, "lng": -75.478158},{"identificador":"4","lat": 10.391707, "lng": -75.479040}, {"identificador":"1","lat": 10.3790921, "lng": -75.4738238}]')) = '3';
  RAISE NOTICE 'La prueba 3 arrojo un %', test3;

  return (test1 and test2 and test3);
end;
$$
language plpgsql;

select unit_test();
