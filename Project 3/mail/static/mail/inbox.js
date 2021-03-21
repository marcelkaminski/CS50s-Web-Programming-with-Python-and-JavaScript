document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(element => {
      if (mailbox != "sent") {
        sender_recipients = element.sender;
      } else {
        sender_recipients = element.recipients;
      }
      if (mailbox == "inbox") {
        if (element.read) is_read = "read";
        else is_read = "";
      } else is_read = "";
      var item = document.createElement("div");
      item.className = `card   ${is_read} my-1 items`;
      item.innerHTML = `<div class="card-body" id="item-${element.id}">
          ${element.subject} | ${sender_recipients} | ${element.timestamp}
          <br>
          ${element.body.slice(0, 100)}
          </div>`;
      document.querySelector("#emails-view").appendChild(item);
      item.addEventListener("click", () => {
        show_mail(element.id, mailbox);
      });
    });
  });
}

function send_email(event) {
  // Don't reload page after submitting
  event.preventDefault();

  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
  .then(load_mailbox("sent"));
}

function show_mail(id, mailbox) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      document.querySelector("#emails-view").innerHTML = "";
      var item = document.createElement("div");
      item.className = `card`;
      item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
      Sender: ${email.sender}
      Recipients: ${email.recipients}
      Subject: ${email.subject}
      Time: ${email.timestamp}
      <br>${email.body}
      </div>`;
      document.querySelector("#emails-view").appendChild(item);
      if (mailbox == "sent") return;
      let archive = document.createElement("btn");
      archive.className = `btn btn-outline-info my-2`;
      archive.addEventListener("click", () => {
        toggle_archive(id, email.archived);
        if (archive.innerText == "Archive") archive.innerText = "Unarchive";
        else archive.innerText = "Archive";
      });
      if (!email.archived) archive.textContent = "Archive";
      else archive.textContent = "Unarchive";
      document.querySelector("#emails-view").appendChild(archive);

      let reply = document.createElement("btn");
      reply.className = `btn btn-outline-success m-2`;
      reply.textContent = "Reply";
      reply.addEventListener("click", () => {
        reply_mail(email.sender, email.subject, email.body, email.timestamp);
      });
      document.querySelector("#emails-view").appendChild(reply);
      make_read(id);
    });
}