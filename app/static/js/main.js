document.addEventListener("DOMContentLoaded", () => {

    // Menú de navegación para dispositivos móviles
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", () => {
            const isOpen = navMenu.classList.toggle("open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        navMenu.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                navMenu.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    // Filtro de categorías de la carta
    const filterButtons = document.querySelectorAll(".filter-btn");
    const menuCards = document.querySelectorAll(".menu-card");
    menuCards.forEach((card, index) => { card.dataset.originalOrder = String(index); });
    const menuSearch = document.getElementById("menuSearch");
    const menuNoResults = document.getElementById("menuNoResults");
    const menuResultCount = document.getElementById("menuResultCount");
    const menuSort = document.getElementById("menuSort");
    const favoritesFilter = document.getElementById("favoritesFilter");
    const favoritesStorageKey = "chifa-fusion-favorites";
    let favorites = new Set();
    try {
        favorites = new Set(JSON.parse(localStorage.getItem(favoritesStorageKey) || "[]"));
    } catch (error) {
        // Keep the carta usable when browser storage is disabled.
    }

    const favoriteButtons = document.querySelectorAll(".favorite-button");
    const syncFavoriteButtons = () => favoriteButtons.forEach(button => {
        const card = button.closest(".menu-card");
        const isFavorite = favorites.has(card.dataset.dishId);
        button.setAttribute("aria-pressed", String(isFavorite));
        button.textContent = isFavorite ? "♥" : "♡";
        button.setAttribute("aria-label", `${isFavorite ? "Quitar" : "Guardar"} ${card.querySelector("h3").textContent} ${isFavorite ? "de" : "en"} favoritos`);
    });

    const updateMenu = () => {
        const activeFilter = document.querySelector(".filter-btn.active")?.dataset.filter || "all";
        const normalize = value => value.toLocaleLowerCase("es").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        const query = normalize(menuSearch?.value.trim() || "");
        const onlyFavorites = favoritesFilter?.getAttribute("aria-pressed") === "true";
        let visibleCount = 0;

        menuCards.forEach(card => {
            const matchesCategory = activeFilter === "all" || card.dataset.category === activeFilter;
            const matchesSearch = normalize(card.textContent).includes(query);
            const matchesFavorite = !onlyFavorites || favorites.has(card.dataset.dishId);
            const visible = matchesCategory && matchesSearch && matchesFavorite;
            card.classList.toggle("hidden", !visible);
            if (visible) visibleCount += 1;
        });

        if (menuNoResults) menuNoResults.hidden = visibleCount > 0;
        if (menuResultCount) {
            menuResultCount.textContent = `${visibleCount} ${visibleCount === 1 ? "plato" : "platos"}`;
        }
    };

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            filterButtons.forEach(item => item.classList.remove("active"));
            button.classList.add("active");
            filterButtons.forEach(item => item.setAttribute("aria-pressed", String(item === button)));
            updateMenu();
        });
    });

    menuSearch?.addEventListener("input", updateMenu);
    if (menuCards.length) updateMenu();

    favoriteButtons.forEach(button => button.addEventListener("click", () => {
        const card = button.closest(".menu-card");
        const id = card.dataset.dishId;
        if (favorites.has(id)) favorites.delete(id);
        else favorites.add(id);
        try {
            localStorage.setItem(favoritesStorageKey, JSON.stringify([...favorites]));
        } catch (error) {
            // Favorites remain active for this visit if storage is unavailable.
        }
        syncFavoriteButtons();
        updateMenu();
    }));

    favoritesFilter?.addEventListener("click", () => {
        const isPressed = favoritesFilter.getAttribute("aria-pressed") === "true";
        favoritesFilter.setAttribute("aria-pressed", String(!isPressed));
        favoritesFilter.querySelector("span").textContent = isPressed ? "Ver favoritos" : "Ver toda la carta";
        updateMenu();
    });
    syncFavoriteButtons();

    menuSort?.addEventListener("change", () => {
        const grid = document.querySelector(".menu-grid");
        if (!grid) return;
        const cards = [...grid.querySelectorAll(".menu-card")];
        const mode = menuSort.value;
        const normalize = value => value.toLocaleLowerCase("es").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        cards.sort((first, second) => {
            if (mode === "name") return normalize(first.querySelector("h3").textContent).localeCompare(normalize(second.querySelector("h3").textContent), "es");
            if (mode === "price-asc" || mode === "price-desc") {
                const a = first.dataset.price === "" ? Number.POSITIVE_INFINITY : Number(first.dataset.price);
                const b = second.dataset.price === "" ? Number.POSITIVE_INFINITY : Number(second.dataset.price);
                return mode === "price-asc" ? a - b : b - a;
            }
            return first.dataset.originalOrder - second.dataset.originalOrder;
        });
        cards.forEach(card => grid.append(card));
    });

    // Evitar seleccionar fechas anteriores al día actual
    const fechaReserva = document.getElementById("fecha_reserva");

    if (fechaReserva) {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, "0");
        const dia = String(hoy.getDate()).padStart(2, "0");

        fechaReserva.min = `${anio}-${mes}-${dia}`;
    }

    const reservationSummary = document.getElementById("reservationSummary");
    if (reservationSummary) {
        const dateField = document.getElementById("fecha_reserva");
        const timeField = document.getElementById("hora_reserva");
        const peopleField = document.getElementById("numero_personas");
        const updateSummary = () => {
            if (!dateField.value && !timeField.value && !peopleField.value) {
                reservationSummary.textContent = "Elige una fecha, hora y cantidad de personas para ver el resumen de tu solicitud.";
                return;
            }
            const date = dateField.value ? new Date(`${dateField.value}T12:00:00`).toLocaleDateString("es-PE", { dateStyle: "long" }) : "fecha por elegir";
            const time = timeField.value || "hora por elegir";
            const people = peopleField.value ? `${peopleField.value} ${Number(peopleField.value) === 1 ? "persona" : "personas"}` : "cantidad por elegir";
            reservationSummary.textContent = `Tu solicitud: ${date}, ${time}, para ${people}.`;
        };
        [dateField, timeField, peopleField].forEach(field => field.addEventListener("change", updateSummary));
    }

    const galleryImages = document.querySelectorAll(".gallery-grid img[role='button']");
    const galleryFilters = document.querySelectorAll(".gallery-filter");
    galleryFilters.forEach(button => button.addEventListener("click", () => {
        const filter = button.dataset.galleryFilter;
        galleryFilters.forEach(item => {
            const active = item === button;
            item.classList.toggle("active", active);
            item.setAttribute("aria-pressed", String(active));
        });
        galleryImages.forEach(image => {
            image.classList.toggle("gallery-hidden", filter !== "all" && image.dataset.galleryCategory !== filter);
        });
    }));

    if (galleryImages.length) {
        const lightbox = document.createElement("dialog");
        lightbox.className = "gallery-lightbox";
        lightbox.setAttribute("aria-label", "Vista ampliada de la galería");
        lightbox.innerHTML = '<button type="button" class="lightbox-close" aria-label="Cerrar imagen">×</button><img alt="">';
        document.body.append(lightbox);
        const lightboxImage = lightbox.querySelector("img");
        const closeButton = lightbox.querySelector(".lightbox-close");

        const openImage = image => {
            lightboxImage.src = image.currentSrc || image.src;
            lightboxImage.alt = image.alt;
            lightbox.showModal();
        };
        galleryImages.forEach(image => {
            image.addEventListener("click", () => openImage(image));
            image.addEventListener("keydown", event => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    openImage(image);
                }
            });
        });
        closeButton.addEventListener("click", () => lightbox.close());
        lightbox.addEventListener("click", event => {
            if (event.target === lightbox) lightbox.close();
        });
    }

    const contactMessage = document.getElementById("mensaje");
    const messageCount = document.getElementById("messageCount");
    if (contactMessage && messageCount) {
        const updateMessageCount = () => { messageCount.textContent = String(contactMessage.value.length); };
        contactMessage.addEventListener("input", updateMessageCount);
        updateMessageCount();
    }

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduceMotion && "IntersectionObserver" in window) {
        const revealTargets = document.querySelectorAll(
            "main > .section, main > .features, main > .event-section, main > .testimonial, main > .about-cta, main > .gallery-cta, main > .promotion-hero, .promotion-cta, .home-highlights article, .story-values article, .menu-card, .promotion-card, .gallery-grid img, .faq-list details"
        );
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });
        revealTargets.forEach((element, index) => {
            element.classList.add("reveal");
            element.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 70}ms`);
            revealObserver.observe(element);
        });
    }

    // Desaparecer avisos después de unos segundos
    document.querySelectorAll(".flash-message").forEach(mensaje => {
        setTimeout(() => {
            mensaje.style.opacity = "0";
            mensaje.style.transition = "opacity .5s";

            setTimeout(() => mensaje.remove(), 500);
        }, 5000);
    });

});
