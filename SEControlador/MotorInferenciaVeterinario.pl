/* Sistema Experto: TuBuenAmigoVeterinario.pl
   Trata los síntomas como una lista. La cabeza es el diagnostico y la “cola” son
   los síntomas.
   Utiliza assert/1 para cambiar dinamicamente la base de conocimientos.
   Determina la verdad y falsedad de los sintomas conocidos.
   Puede contestar a las preguntas 'porque' e incluye capacidad de explicacion.
   Elimina dinamicamente las aseveraciones agregadas despues de cada consulta.
*/

% Declaracion de predicados dinamicos. Para que se registren las respuestas del usuario como hechos temporales.
:- dynamic conocido/1. % Es esencial para el uso de asserta/1 y retract/1.

% Predicado de entrada y control de flujo. Para inicia la consulta del usuario, generar el diagnóstico, mostrarlo y preguntar por una explicación.
consulta :-
    haz_diagnostico(X), % Genera un diagnóstico basado en los síntomas conocidos (confirmados).
    escribe_diagnostico(X), % Muestra el diagnóstico.
    ofrece_explicacion_diagnostico(X), % Pregunta si se desea una explicacion del diagnostico.
    clean_scratchpad. % Limpia la memoria temporal.

% Predicado de manejo de fallos. Si no se puede generar un diagnóstico, informa al usuario y limpia la memoria temporal.
consulta :-
    write('No hay suficiente conocimiento para elaborar un diagnostico.'), % Mensaje de fallo.
    clean_scratchpad. % Limpia la memoria temporal.

% Predicado para generar un diagnóstico basado en los síntomas conocidos.
haz_diagnostico(Diagnosis) :-
    obten_hipotesis_y_sintomas(Diagnosis, ListaDeSintomas), % Obtiene una hipótesis (diagnóstico) y su lista de síntomas asociados a la enfermedad. Permite backtracking en caso de falla
    prueba_presencia_de(Diagnosis, ListaDeSintomas). % Verifica si todos los síntomas están presentes acordes a la enfermedad.

obten_hipotesis_y_sintomas(Diagnosis, ListaDeSintomas) :-
    conocimiento(Diagnosis, ListaDeSintomas).

prueba_presencia_de(_Diagnosis, []).

% Predicados para verificar recursivamente la presencia de cada síntoma en la lista.
prueba_presencia_de(Diagnosis, [Head | Tail]) :-
    prueba_verdad_de(Diagnosis, Head), % Verifica si el síntoma actual es verdadero (conocido).
    prueba_presencia_de(Diagnosis, Tail). % Continúa con el siguiente síntoma en la lista.

% Predicados para verificar si un síntoma es conocido (verdadero) o pregunta al usuario si no lo es.
prueba_verdad_de(_Diagnosis, Sintoma) :-
    conocido(Sintoma). % Si el síntoma ya es conocido como verdadero, no se necesita preguntar nuevamente.

% Si el síntoma no es conocido como falso, pregunta al usuario sobre su presencia.
prueba_verdad_de(Diagnosis, Sintoma) :-
    not(conocido(is_false(Sintoma))), % Asegura que el síntoma no ha sido conocido como falso.
    pregunta_sobre(Diagnosis, Sintoma, Reply), % Pregunta al usuario sobre el síntoma a confirmar.
    Reply = si.

% Maneja la interación con el usuario para confirmar la presencia de un síntoma.
pregunta_sobre(Diagnosis, Sintoma, Reply) :-
    write('Tú felino presenta '), % Pregunta al usuario sobre el síntoma.
    write(Sintoma), write('? '), % Muestra el síntoma.
    read(Respuesta), % Lee la respuesta del usuario.
    process(Diagnosis, Sintoma, Respuesta, Reply). % Procesa la respuesta del usuario.

% Procesa la respuesta del usuario y actualiza la base de conocimientos temporalmente.
process(_Diagnosis, Sintoma, si, si) :-
    asserta(conocido(Sintoma)). % Si el usuario confirma el síntoma, lo registra como conocido en la base de conocimiento.

% Procesa la respuesta negativa del usuario.
process(_Diagnosis, Sintoma, no, no) :-
    asserta(conocido(is_false(Sintoma))). % Si el usuario niega el síntoma, lo registra como falso en la base de conocimiento.

% Procesa la solicitud de explicación del usuario.
process(Diagnosis, Sintoma, porque, Reply) :-
    nl, % Nueva línea para claridad del mensaje de la solicitud del usuario.
    write('Estoy investigando la hipotesis siguiente: '), % Muestra la hipótesis actual.
    write(Diagnosis), write('.'), nl, % Nueva línea con la enfermedad asociada a la hipótesis planteada.
    write('Para esto necesito saber si '), % Pregunta por el síntoma específico.
    write(Sintoma), write('.'), nl, % Nueva línea con el síntoma en cuestión.
    pregunta_sobre(Diagnosis, Sintoma, Reply). % Vuelve a preguntar sobre el síntoma para obtener una respuesta válida.

% Maneja respuestas inválidas del usuario, solo validas si, no y porque.
process(Diagnosis, Sintoma, Respuesta, Reply) :-
    Respuesta \== no,
    Respuesta \== si,
    Respuesta \== porque, nl,
    write('Debes contestar si, no o porque.'), nl,
    pregunta_sobre(Diagnosis, Sintoma, Reply).

% Muestra el diagnóstico al usuario.
escribe_diagnostico(Diagnosis) :-
    write('El diagnostico es '),
    write(Diagnosis), write('.'), nl. % Nueva línea para claridad de la enfermedad detectada.

% Ofrece una explicación del diagnóstico si el usuario lo solicita.
ofrece_explicacion_diagnostico(Diagnosis) :-
    pregunta_si_necesita_explicacion(Respuesta), % Pregunta al usuario si desea una explicación del diagnóstico.
    actua_consecuentemente(Diagnosis, Respuesta). % Actúa según la respuesta del usuario.

% Pregunta al usuario si desea una explicación del diagnóstico (justificación).
pregunta_si_necesita_explicacion(Respuesta) :-
    write('Quieres que justifique este diagnostico? '),
    read(RespuestaUsuario), % Lee la respuesta del usuario.
    asegura_respuesta_si_o_no(RespuestaUsuario, Respuesta). % Asegura que la respuesta sea válida (si o no).

% Asegura que la respuesta del usuario sea válida (si o no).
asegura_respuesta_si_o_no(si, si). % Predicado
asegura_respuesta_si_o_no(no, no).
asegura_respuesta_si_o_no(_, Respuesta) :-
    write('Debes contestar si o no.'),
    pregunta_si_necesita_explicacion(Respuesta).

% Actúa según la respuesta del usuario para proporcionar o no la explicación (justificación).
actua_consecuentemente(_Diagnosis, no).

% Proporciona la explicación del diagnóstico mostrando los síntomas asociados.
actua_consecuentemente(Diagnosis, si) :-
    conocimiento(Diagnosis, ListaDeSintomas),
    write('Se determino este diagnostico porque se encontraron los siguentes sintomas: '), nl,
    escribe_lista_de_sintomas(ListaDeSintomas),
    nl, % Añadimos un espacio
    mostrar_causas(Diagnosis). % Llamamos a un nuevo predicado para la causa

% Predicado para mostrar la causa del diagnóstico.
mostrar_causas(Diagnosis) :-
    causas(Diagnosis, ListaDeCausas), !, % El '!' (corte) evita buscar mas causas si hay varias, evitando buscar otros hechos.
    write('La(s) causa(s) comunes de esta enfermedad es: '), nl,
    escribe_lista_causas(ListaDeCausas).
mostrar_causas(_). % Si (no hay causa en la BC), este predicado simplemente tiene éxito en silencio, no falla.

% Predicado para escribir la lista de causas.
escribe_lista_causas([]).
escribe_lista_causas([Head | Tail]) :-
    write(' - '), write(Head), nl, % Imprime la causa con un guion para formatearla
    escribe_lista_causas(Tail).

% Predicado para escribir la lista de síntomas.
escribe_lista_de_sintomas([]).

% Predicado recursivo para escribir cada síntoma en la lista.
escribe_lista_de_sintomas([Head | Tail]) :-
    write(Head), nl,
    escribe_lista_de_sintomas(Tail).

% Limpia la memoria temporal eliminando todos los hechos conocidos agregados a la base de conocimiento durante la consulta.
clean_scratchpad :-
    retract(conocido(_X)), fail. % Elimina todos los hechos conocidos.
clean_scratchpad.

conocido(_) :- fail. % Inicialmente no hay hechos conocidos.

not(X) :- X, !, fail. % Si X es verdadero, falla.
not(_). % Si X no es verdadero, entonces not(X) es verdadero.