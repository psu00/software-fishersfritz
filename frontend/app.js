// Grund-URL des Backends
const API_URL = "http://127.0.0.1:5000/history/filter";
const CATCH_API_URL = "http://127.0.0.1:5000/catch";

// Funktion: Fische basierend auf Filter laden und rendern (nach Art)
async function renderGroupedByFish(period) {
  try {
    const response = await fetch(`${API_URL}?period=${period}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    const container = document.getElementById("group-by-fish");

    // Container leeren
    container.innerHTML = "";

    // Rendern der Fische (nach Art und Anzahl)
    if (data.by_fish && data.by_fish.length > 0) {
      data.by_fish.forEach((fish) => {
        const fishDiv = `
          <div class="fish-card">
            <h5>${fish.fish_name}</h5>
            <p>Anzahl: ${fish.count}</p>
          </div>`;
        container.innerHTML += fishDiv;
      });
    } else {
      container.innerHTML = "<p>Keine Fänge für diesen Zeitraum</p>";
    }
  } catch (error) {
    console.error("Fehler beim Laden der Fische nach Art:", error);
    const container = document.getElementById("group-by-fish");
    container.innerHTML = "<p>Fehler beim Laden der Daten</p>";
  }
}

// Funktion: Fische basierend auf Filter laden und rendern (nach Zeit)
async function renderGroupedByDate(period) {
  try {
    const response = await fetch(`${API_URL}?period=${period}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    const container = document.getElementById("group-by-date");

    // Container leeren
    container.innerHTML = "";

    // Fisch Bilder
    const fishImages = {
      "Rotauge": "images/Rotauge.jpg",
      "Brachse": "images/Brachse.jpeg",
      "Hecht": "images/Hecht.jpg",
      "Karpfen": "images/Karpfen.jpg",
      "Zander": "images/Zander.jpg",
      "Wels": "images/Wels.jpg",
      "Flussbarsch": "images/Flussbarsch.jpg",
      "Schleie": "images/Schleie.jpg",
      "Huchen": "images/Huchen.png",
      "Reinanke": "images/Reinanke.jpg",
      "Seeforelle": "images/Seeforelle.jpg"
    };
    

    // Rendern der Fische (nach Datum)
    if (data.by_date) {
      for (const date in data.by_date) {
        const fishItems = data.by_date[date]
          .map(
            (fish) =>
              `<div class="fish-entry" data-catch-id="${fish.catch_id}">
                <img src="${fishImages[fish.fish_name]}" width="75" height="50">  
                 <span>${fish.fish_name}</span>
                 <span>Gewicht: ${fish.weight} kg</span>
                 <button class="btn btn-warning btn-sm" onclick="editCatch(${fish.catch_id})">Bearbeiten</button>
                 <button class="btn btn-danger btn-sm" onclick="deleteCatch(${fish.catch_id})">Löschen</button>
               </div>`
          )
          .join("");

        const dateBlock = `
          <div class="date-group">
            <h5>${date}</h5>
            <div class="fish-entries">${fishItems}</div>
          </div>`;
        container.innerHTML += dateBlock;
      }
    } else {
      container.innerHTML = "<p>Keine Historie für diesen Zeitraum verfügbar</p>";
    }
  } catch (error) {
    console.error("Fehler beim Laden der Historie nach Zeit:", error);
    const container = document.getElementById("group-by-date");
    container.innerHTML = "<p>Fehler beim Laden der Daten</p>";
  }
}

// Funktion: Aktualisiere beide Bereiche (nach Art und nach Zeit)
function updateView(period) {
  renderGroupedByFish(period); // Gruppiert nach Art
  renderGroupedByDate(period); // Gruppiert nach Zeit
}

function resetCatch() {
    const form = document.getElementById("fishCatchForm");
    form.reset(); // Setzt das gesamte Formular zurück
  }

// Funktion: Neuen Fang speichern
async function saveCatch(event) {
  event.preventDefault(); // Verhindere das Standardformular-Verhalten

  // Hole die Eingabedaten aus dem Formular
  const fishName = document.getElementById("fish").value;
  const latitude = document.getElementById("locationname").value.split(",")[0].trim();
  const longitude = document.getElementById("locationname").value.split(",")[1]?.trim();
  const weight = document.getElementById("weight").value;
  const date = document.getElementById("date").value;

  // Überprüfe, ob alle erforderlichen Felder ausgefüllt sind
  if (!fishName || !latitude || !longitude || !weight || !date) {
    alert("Bitte alle erforderlichen Felder ausfüllen.");
    return;
  }

  // JSON-Payload für den POST-Request
  const payload = {
    fish_name: fishName,
    latitude: parseFloat(latitude),
    longitude: parseFloat(longitude),
    weight: parseFloat(weight),
    date: date,
  };

  try {
    // Sende die Daten an das Backend
    const response = await fetch(CATCH_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    // Überprüfe die Antwort
    if (response.ok) {
      alert("Fang erfolgreich gespeichert!");
      document.getElementById("fishCatchForm").reset(); // Formular zurücksetzen
      updateView("total"); // Aktualisiere die Ansicht (total)
    } else {
      const errorData = await response.json();
      alert(`Fehler: ${errorData.error}`);
    }
  } catch (error) {
    console.error("Fehler beim Speichern des Fangs:", error);
    alert("Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.");
  }
}

async function deleteCatch(catchId) {
  if (!catchId) {
    console.error("Die Catch-ID ist undefined.");
    alert("Fehler: Catch-ID fehlt.");
    return;
  }
  const confirmation = confirm("Möchtest du diesen Fang wirklich löschen?");
  if (!confirmation) return;

  try {
    const response = await fetch(`http://127.0.0.1:5000/history/${catchId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      alert("Fang wurde erfolgreich gelöscht!");
      // Entferne den Eintrag aus der Ansicht
      const entry = document.querySelector(`[data-catch-id="${catchId}"]`);
      if (entry) entry.remove();

      // Entferne die Gruppe, wenn keine Einträge mehr vorhanden sind
      const dateGroup = entry.closest(".date-group");
      if (dateGroup && dateGroup.querySelectorAll(".fish-entry").length === 0) {
        dateGroup.remove();
      }
    } else {
      const errorData = await response.json();
      alert(`Fehler: ${errorData.error}`);
    }
  } catch (error) {
    console.error("Fehler beim Löschen des Fangs:", error);
    alert("Ein Fehler ist aufgetreten. Bitte versuche es später erneut.");
  }
}


// Funktion: Fischnamen vom Backend aus der Tabelle Fish laden und im Formular anzeigen
async function loadFishNames() {
  const dropdown = document.getElementById("fish");

  try {
    // Abrufen der Fischnamen vom Backend
    const response = await fetch("http://127.0.0.1:5000/fish");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const fishNames = await response.json();

    // Dropdown-Menü leeren und mit Optionen füllen
    dropdown.innerHTML = '<option value="" disabled selected>Wähle einen Fisch</option>';
    fishNames.forEach((fishName) => {
      const option = document.createElement("option");
      option.value = fishName; // Der Wert der Option
      option.textContent = fishName; // Der angezeigte Text
      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error("Fehler beim Laden der Fischnamen:", error);
    dropdown.innerHTML = '<option value="" disabled>Fischnamen konnten nicht geladen werden</option>';
  }
}

async function editCatch(catchId) {
  try {
    // Daten für die spezifische ID abrufen
    const response = await fetch(`http://127.0.0.1:5000/history/${catchId}`);
    if (!response.ok) {
      throw new Error(`Fehler beim Abrufen der Daten: ${response.status}`);
    }

    const data = await response.json();

    // Canvas öffnen und die Formularfelder mit den abgerufenen Daten füllen
    const offcanvas = new bootstrap.Offcanvas(document.getElementById("offcanvasFishCatch"));
    offcanvas.show();

    document.getElementById("fish").value = data.fish_name;
    document.getElementById("locationname").value = `${data.latitude}, ${data.longitude}`;
    document.getElementById("date").value = data.date;
    document.getElementById("weight").value = data.weight;
    document.getElementById("length").value = data.length || ""; // Falls Länge nicht verfügbar, leer lassen

    // Speichern-Button aktualisieren
    const saveButton = document.querySelector("#fishCatchForm button[type='submit']");
    saveButton.setAttribute("onclick", `saveEdit(${catchId})`);
  } catch (error) {
    console.error("Fehler beim Laden der Daten:", error);
    alert("Ein Fehler ist aufgetreten. Bitte versuche es später erneut.");
  }
}

async function saveEdit(catchId) {
  const fishName = document.getElementById("fish").value;
  const latitude = document.getElementById("locationname").value.split(",")[0].trim();
  const longitude = document.getElementById("locationname").value.split(",")[1]?.trim();
  const weight = document.getElementById("weight").value;
  const date = document.getElementById("date").value;
  const length = document.getElementById("length").value;

  // Überprüfen, ob alle Felder ausgefüllt sind
  if (!fishName || !latitude || !longitude || !weight || !date) {
    alert("Bitte alle erforderlichen Felder ausfüllen.");
    return;
  }

  // JSON-Payload für den PUT-Request
  const payload = {
    fish_name: fishName,
    latitude: parseFloat(latitude),
    longitude: parseFloat(longitude),
    weight: parseFloat(weight),
    date: date,
    length: length ? parseFloat(length) : null, // Optionales Feld
  };

  try {
    // Sende die aktualisierten Daten an das Backend
    const response = await fetch(`http://127.0.0.1:5000/history/${catchId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      alert("Fang erfolgreich aktualisiert!");
      document.getElementById("fishCatchForm").reset(); // Formular zurücksetzen
      const offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById("offcanvasFishCatch"));
      offcanvas.hide(); // Canvas schließen
      updateView("total"); // Ansicht aktualisieren
    } else {
      const errorData = await response.json();
      alert(`Fehler: ${errorData.error}`);
    }
  } catch (error) {
    console.error("Fehler beim Aktualisieren des Fangs:", error);
    alert("Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.");
  }
}




// Funktion, um die Uhrzeit ins Formular zu setzen
function setCurrentTime() {
    const timeInput = document.getElementById("time");
    if (timeInput) {
      // Aktuelle Uhrzeit im Format HH:MM holen
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, "0");
      const minutes = now.getMinutes().toString().padStart(2, "0");
      const currentTime = `${hours}:${minutes}`;
  
      // Uhrzeit in das Eingabefeld setzen
      timeInput.value = currentTime;
    }
  }

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;
  
          // Setze die Koordinaten in das Eingabefeld
          document.getElementById("locationname").value = `${latitude}, ${longitude}`;
        },
        (error) => {
          console.error("Fehler beim Abrufen der Position:", error.message);
          alert("Konnte den Standort nicht abrufen. Bitte Standortdienste aktivieren.");
        }
      );
    } else {
      alert("Geolocation wird von deinem Browser nicht unterstützt.");
    }
  }
  

// Event-Listener für die Radiobuttons
document.addEventListener("DOMContentLoaded", () => {
  // Standardansicht (Total)
  updateView("total");
  // Funktion, um die aktuelle Uhrzeit in das Formular einzufügen
  setCurrentTime();

  // Event-Listener für Radiobuttons hinzufügen
  const radioButtons = document.querySelectorAll("input[name='btnradio']");
  radioButtons.forEach((button) => {
    button.addEventListener("change", (event) => {
      const period = event.target.id.replace("btnradio", "").toLowerCase(); // z.B. "d", "w", "m", "y", "t"
      const periodMap = {
        d: "1day",
        w: "1week",
        m: "1month",
        y: "1year",
        t: "total",
      };
      updateView(periodMap[period]);
    });
  });

  // Event-Listener für das Formular zum Speichern eines neuen Fangs
  const form = document.getElementById("fishCatchForm");
  form.addEventListener("submit", saveCatch);
});

// Event-Listener: Fische laden, wenn die Seite geladen wird
document.addEventListener("DOMContentLoaded", loadFishNames);
