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

    // Rendern der Fische (nach Datum)
    if (data.by_date) {
      for (const date in data.by_date) {
        const fishItems = data.by_date[date]
          .map(
            (fish) =>
              `<div class="fish-entry">
                 <span>${fish.fish_name}</span>
                 <span>Gewicht: ${fish.weight} kg</span>
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

// Event-Listener: Fische laden, wenn die Seite geladen wird
document.addEventListener("DOMContentLoaded", loadFishNames);

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
