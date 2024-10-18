// Consumo de API

const listaUsuarios = async () => {
  const respuesta = await fetch("https://jsonplaceholder.typicode.com/users");
  const users = await respuesta.json();

  let tableBody = ``;
  users.forEach((user, index) => {
    tableBody += `<tr>
    <td>${user.name}</td>
    <td>${user.email}</td>
    </tr>`;
  });
  tableBody_Users.innerHTML = tableBody;
}

window.addEventListener("load", function () {
    listaUsuarios();
});
