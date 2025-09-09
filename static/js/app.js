const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");

function appendMessage(text, cls){
  const div = document.createElement("div");
  div.className = "message " + cls;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendTyping(){
  const div = document.createElement("div");
  div.className = "typing";
  div.innerHTML = `<span></span><span></span><span></span>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  const msg = input.value.trim();
  if(!msg) return;
  appendMessage(msg,"user");
  input.value="";
  const typingDiv = appendTyping();
  try{
    const res = await fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({message:msg})
    });
    const data = await res.json();
    typingDiv.remove();
    appendMessage(data.reply,"bot");
  } catch(err){
    typingDiv.remove();
    appendMessage("⚠️ Network error","bot");
  }
});
