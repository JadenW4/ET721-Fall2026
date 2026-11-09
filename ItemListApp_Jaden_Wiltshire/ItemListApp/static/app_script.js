const form = document.querySelector('#itemForm');
const money = value => '$' + Number(value).toFixed(2);
form.addEventListener('submit', async event => {
  event.preventDefault();
  const name = document.querySelector('#name').value.trim();
  const price = Number(document.querySelector('#price').value);
  const response = document.querySelector('#response');
  try {
    const res = await fetch('/items', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name, price})});
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Unable to add item');
    response.textContent = `✓ Added ${data.item.name} (${money(data.item.price)})`;
    form.reset();
    await loaditems();
  } catch(error) {response.textContent = 'Error: ' + error.message;}
});
async function loaditems() {
  const list = document.querySelector('.itemslist');
  try {
    const res = await fetch('/items');
    if (!res.ok) throw new Error('Unable to load items');
    const data = await res.json();
    const entries = Object.entries(data);
    document.querySelector('#itemCount').textContent = entries.length;
    list.replaceChildren();
    if (!entries.length) {const li=document.createElement('li'); li.className='empty'; li.textContent='No items yet. Add one using the form.'; list.append(li); return;}
    for (const [id, item] of entries) {
      const li=document.createElement('li'); li.className='item-row';
      const info=document.createElement('div'); info.className='item-info';
      const idTag=document.createElement('span'); idTag.className='item-id'; idTag.textContent='ITEM #'+id;
      const name=document.createElement('strong'); name.textContent=item.name;
      const price=document.createElement('span'); price.className='price'; price.textContent=money(item.price);
      info.append(idTag,name,price);
      const actions=document.createElement('div'); actions.className='actions';
      const edit=document.createElement('button'); edit.className='btn edit'; edit.textContent='Edit'; edit.onclick=()=>showupdateform(id,item.name,item.price);
      const del=document.createElement('button'); del.className='btn danger'; del.textContent='Delete'; del.onclick=()=>deleteitem(id);
      actions.append(edit,del); li.append(info,actions); list.append(li);
    }
  } catch(error) {list.textContent='Error: '+error.message;}
}
function showupdateform(id,name,price) {
  const section=document.querySelector('#updatasection'); section.hidden=false;
  document.querySelector('#updateID').value=id;
  document.querySelector('#updateName').value=name;
  document.querySelector('#updatePrice').value=price;
  section.scrollIntoView({behavior:'smooth',block:'center'});
}
function hideUpdateForm(){document.querySelector('#updatasection').hidden=true;}
async function updateItem(){
  const id=document.querySelector('#updateID').value;
  const name=document.querySelector('#updateName').value.trim();
  const price=Number(document.querySelector('#updatePrice').value);
  if (!name || !document.querySelector('#updatePrice').value || price<0) {alert('Enter a valid name and price.');return;}
  try {
    const res=await fetch(`/items/${encodeURIComponent(id)}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,price})});
    const html=await res.text(); document.open();document.write(html);document.close();
  } catch(error){alert('Update failed: '+error.message);}
}
async function deleteitem(id){
  if (!confirm('Delete item #'+id+'?')) return;
  try {const res=await fetch(`/items/${encodeURIComponent(id)}`,{method:'DELETE'});const html=await res.text();document.open();document.write(html);document.close();}
  catch(error){alert('Delete failed: '+error.message);}
}
