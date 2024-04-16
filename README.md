## Índice

- [Funcionalidades](#Funcionalidades)
- [Rotas](#Rotas)
- [Models](#Models)


## Funcionalidades
Nossa API backend REST foi projetada para uma aplicação de To-Do list. O sistema é capaz de criar, autênticar e autorizar um usuário, além disso, possui a funcionalidade de criar uma To-Do list, assim como criar To-Dos e associa-las á uma Lista.

Usuário (CRUD) - Criar, editar dados, ler dados e deletar um usuário

Todo-List (CRUD) - Criar, editar dados, ler dados e deletar uma To-Do List ou To-Do

## Rotas
<h3>Rotas de usuário</h3>
http://127.0.0.1:8000/authenticate/register - Recebe POST com username, password e email(opcional)

<br>
http://127.0.0.1:8000/authenticate/login - Recebe POST com username, password e email(opcional)

<br>
http://127.0.0.1:8000/authenticate/authtoken - Recebe um POST com um token e verifica se pertence á um usuário válido no banco de dados.
<h3>Rotas de Todo e TodoList</h3>
<p>As rotas á seguir necessitam de autenticação. Envie um Header na requisição no seguinte formato: "Authorization: Token xxxxxxxxxxx"</p>
http://127.0.0.1:8000/todolists - Recebe um GET que retorna todas as TodoLists e Todos associadas á um usuário.

<br>
http://127.0.0.1:8000/todolistnew - Recebe um POST que cria uma nova TodoList. Necessita do parâmetro "title" no body da requisição.

<br>
http://127.0.0.1:8000/todonew - Recebe POST, PUT ou DELETE que cria, altera ou deleta uma Todo. No caso do Put e do Delete o parâmetro todoId é necessário. Já no Post, é exigido apenas o parâmetro todoList com o nome de alguma To-Do List existente.

## Models
Segue o Model de TodoList<br>
<ul>
    <li>
    user : Usuário dono da TodoList
    </li>
    <li>
    title : Charfield de no máximo 30 caracteres
    </li>
</ul>
Segue o Model de Todo<br>
<ul>
    <li>
    todoList : Todo List á qual o Todo pertence
    </li>
    <li>
    title : Charfield de no máximo 30 caracteres
    </li>
    <li>
    description : Charfield de no máximo 500 caracteres
    </li>
    <li>
    complete : Booleano que sinaliza se a To-Do foi completa
    </li>
    <li>
    create : DateTime que armazena a hora que a To-Do foi criada
    </li>
</ul>

<h2>Obrigado!</h2>
