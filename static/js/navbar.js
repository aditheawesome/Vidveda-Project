const burger = document.querySelector('.hamburger');
const list = document.querySelector('.list');
const main = document.querySelector('main');


burger.addEventListener("click", () => {
    list.classList.toggle("list-toggle");
    burger.classList.toggle("ham-active");


})




main.addEventListener("click", function change() {

    
        list.classList.remove("list-toggle");
        burger.classList.remove("ham-active");


    
})


let resizeTimer;
window.addEventListener("resize", () => {
  document.body.classList.add("resize-animation-stopper");
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    document.body.classList.remove("resize-animation-stopper");
  }, 400);
});