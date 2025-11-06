
    const mainImage = document.getElementById("mainImage");
    const zoomLens = document.getElementById("zoomLens");
    const thumbnails = document.querySelectorAll(".thumbnail-row img");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");

    let currentIndex = 0;

    thumbnails.forEach((thumb, index) => {
      thumb.addEventListener("click", () => {
        thumbnails.forEach(t => t.classList.remove("active"));
        thumb.classList.add("active");
        mainImage.src = thumb.src;
        zoomLens.style.backgroundImage = `url(${thumb.src})`;
        currentIndex = index;
      });
    });

    nextBtn.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % thumbnails.length;
      updateMainImage();
    });

    prevBtn.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
      updateMainImage();
    });

    function updateMainImage() {
      thumbnails.forEach(t => t.classList.remove("active"));
      thumbnails[currentIndex].classList.add("active");
      const src = thumbnails[currentIndex].src;
      mainImage.src = src;
      zoomLens.style.backgroundImage = `url(${src})`;
    }

    // Hover zoom behavior
    const container = document.getElementById("mainImageContainer");

    container.addEventListener("mouseenter", () => {
      zoomLens.style.display = "block";
      zoomLens.style.backgroundImage = `url(${mainImage.src})`;
    });

    container.addEventListener("mousemove", (e) => {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const xPercent = (x / rect.width) * 100;
      const yPercent = (y / rect.height) * 100;
      zoomLens.style.backgroundPosition = `${xPercent}% ${yPercent}%`;
    });

    container.addEventListener("mouseleave", () => {
      zoomLens.style.display = "none";
    });



    // === Initialize first thumbnail as default main image ===
window.addEventListener("DOMContentLoaded", () => {
  thumbnails.forEach(t => t.classList.remove("active"));
  thumbnails[0].classList.add("active");

  const firstSrc = thumbnails[0].src;
  mainImage.src = firstSrc;
  zoomLens.style.backgroundImage = `url(${firstSrc})`;
  currentIndex = 0;
});
