document.addEventListener("DOMContentLoaded", () => {
  document.body.style.opacity = 0;
  setTimeout(() => { document.body.style.transition = "opacity 1s"; document.body.style.opacity = 1; }, 100);

  const form = document.getElementById("uploadForm");
  const progressSection = document.getElementById("progressSection");
  const progressFill = document.getElementById("progressFill");
  const progressValue = document.getElementById("progressValue");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      progressSection.classList.remove("hidden");
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.floor(Math.random()*10)+5;
        if(progress>100) progress=100;
        progressFill.style.width = progress + "%";
        progressValue.textContent = progress + "%";
        if(progress===100){
          clearInterval(interval);
          setTimeout(()=>{form.submit();},500);
        }
      }, 300);
    });
  }
});
