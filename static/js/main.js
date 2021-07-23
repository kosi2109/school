const btn = document.querySelectorAll(".menu div");
const sec = document.querySelectorAll("section");



if (localStorage.getItem('active') != null){
  ac = localStorage.getItem('active')
  document.querySelector("#" + ac).classList.add("active");
}else{
  
 localStorage.setItem('active','home')
}
btn.forEach((b) => {

  b.addEventListener("click", () => {
    var Id = b.dataset.section;
    sec.forEach((s) => {
      var current = "#" + s.id;
      var currentClick = "#" + Id;
      if (current == currentClick) {
        localStorage.setItem('active', ''+Id)
        var ac = localStorage.getItem('active')
        var section = document.querySelector("#" + ac);
        
        var ac = localStorage.getItem('active')
        window.history.pushState({ urlPath: `#${ac}` }, "", `#${ac}`);
        section.classList.add("active");
      } else {
        s.classList.remove("active");
      }
    });
  });
});


const form = document.querySelector('.create-form')
const formBtn = document.getElementById('form-btn')

formBtn.addEventListener('click',()=>{
  console.log('c')
  form.classList.toggle('form-active')
})





  