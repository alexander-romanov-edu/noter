async function loadExercises() {
    const res = await fetch(`${API}/exercises/`);
    const data = await res.json();

    log(JSON.stringify(data, null, 2));
}

async function addExercise() {
    const name = document.getElementById("exercise").value;

    await fetch(`${API}/exercises/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });

    loadExercises();
}
let currentSession = null;
let exercises = [];

// load exercises into dropdown
async function loadExercises() {
    const res = await fetch(`${API}/exercises/`);
    exercises = await res.json();

    const select = document.getElementById("exerciseSelect");
    select.innerHTML = "";

    exercises.forEach(ex => {
        const option = document.createElement("option");
        option.value = ex.id;
        option.text = ex.name;
        select.appendChild(option);
    });

    log("Exercises loaded");
}

// start workout
async function startSession() {
    const res = await fetch(`${API}/sessions/`, {
        method: "POST"
    });

    const data = await res.json();
    currentSession = data.id;

    document.getElementById("sessionInfo").innerText =
        `Active session ID: ${currentSession}`;
}

// add set
async function addSet() {
    if (!currentSession) {
        log("Start a session first!");
        return;
    }

    const exercise_id = document.getElementById("exerciseSelect").value;
    const weight = parseInt(document.getElementById("weight").value);
    const reps = parseInt(document.getElementById("reps").value);

    const res = await fetch(`${API}/sets/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            session_id: currentSession,
            exercise_id,
            weight,
            reps
        })
    });

    const data = await res.json();

    loadSets();
}

// load sets for current session
async function loadSets() {
    if (!currentSession) return;

    const res = await fetch(`${API}/sets/`);
    const allSets = await res.json();

    const filtered = allSets.filter(s => s.session_id === currentSession);

    document.getElementById("setsOutput").innerText =
        JSON.stringify(filtered, null, 2);
}
