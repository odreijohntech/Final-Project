<script lang="ts">
  import { onMount } from "svelte";
  import { ArrowRight, Check, ChevronDown, CircleHelp, LoaderCircle, Moon, RotateCcw, Sparkles, Sun } from "@lucide/svelte";

  type Profile = { age: number; sex: string; famsize: string; Medu: number; Fedu: number; studytime: number; failures: number; higher: string; internet: string; famrel: number; freetime: number; health: number; absences: number; G1: number; G2: number };
  type Prediction = { predicted_grade: number; percentage: string; pass_fail: "PASS" | "FAIL"; status: string };
  const defaults: Profile = { age: 17, sex: "F", famsize: "GT3", Medu: 3, Fedu: 2, studytime: 2, failures: 0, higher: "yes", internet: "yes", famrel: 4, freetime: 3, health: 3, absences: 4, G1: 12, G2: 13 };
  const modelDefaults = { address: "U", guardian: "mother", Mjob: "at_home", Fjob: "teacher", Pstatus: "T", reason: "course", activities: "no", schoolsup: "yes", nursery: "yes", traveltime: 2, paid: "no", famsup: "no", goout: 4, Walc: 1, romantic: "no", Dalc: 1 };

  let profile = $state<Profile>({ ...defaults });
  let prediction = $state<Prediction | null>(null);
  let theme = $state<"light" | "dark">("light");
  let busy = $state(false);
  let errorMessage = $state("");
  const isPass = $derived(prediction?.pass_fail === "PASS");

  onMount(() => {
    const savedTheme = localStorage.getItem("gradepilot-theme");
    if (savedTheme === "light" || savedTheme === "dark") theme = savedTheme;
  });

  function toggleTheme() {
    theme = theme === "light" ? "dark" : "light";
    localStorage.setItem("gradepilot-theme", theme);
  }

  function resetForm() {
    profile = { ...defaults };
    prediction = null;
    errorMessage = "";
  }

  async function predict() {
    busy = true;
    prediction = null;
    errorMessage = "";
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...profile, ...modelDefaults })
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.detail ?? "The prediction service could not process this profile.");
      prediction = body as Prediction;
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : "Unable to reach the prediction service. Please try again.";
    } finally {
      busy = false;
    }
  }

  function insights() {
    const items: { title: string; note: string; positive: boolean }[] = [];
    const recentAverage = (profile.G1 + profile.G2) / 2;
    if (recentAverage >= 13) items.push({ title: "Recent grades are a strength", note: `The average of the two reported periods is ${recentAverage.toFixed(1)}/20.`, positive: true });
    else if (recentAverage < 10) items.push({ title: "Recent grades need attention", note: `The average of the two reported periods is ${recentAverage.toFixed(1)}/20.`, positive: false });
    else items.push({ title: "Recent grades are near the passing mark", note: `The two reported periods average ${recentAverage.toFixed(1)}/20.`, positive: false });
    if (profile.absences > 10) items.push({ title: "Attendance may need support", note: `${profile.absences} absences may reduce time available for learning.`, positive: false });
    else if (profile.absences <= 5) items.push({ title: "Attendance is a positive signal", note: `${profile.absences} absences were reported.`, positive: true });
    if (profile.failures > 0) items.push({ title: "Previous class challenges", note: `${profile.failures} previous class failure(s) may need follow-up.`, positive: false });
    else items.push({ title: "No previous class failures reported", note: "Keep checking progress throughout the term.", positive: true });
    if (profile.studytime <= 1) items.push({ title: "Study routine could use support", note: "The selected study time is under two hours per week.", positive: false });
    else if (profile.studytime >= 3) items.push({ title: "Regular study time", note: "The selected weekly study time is five hours or more.", positive: true });
    return items.slice(0, 3);
  }

  function recommendations() {
    const suggestions: string[] = [];
    if (!isPass) {
      if (profile.G1 < 10 || profile.G2 < 10) suggestions.push("Review the topics behind the lower period grade with a teacher or tutor.");
      if (profile.studytime <= 2) suggestions.push("Set a small, consistent weekly study plan and check progress each week.");
      if (profile.absences > 10) suggestions.push("Discuss attendance barriers and agree on a practical support plan.");
      if (!suggestions.length) suggestions.push("Schedule a supportive check-in and review progress before the next assessment.");
    } else {
      suggestions.push("Maintain the study and attendance habits that are working.");
      suggestions.push("Check progress before the next assessment so support can be offered early.");
    }
    return suggestions.slice(0, 3);
  }
</script>

<svelte:head>
  <title>GradePilot — Advanced Educational Performance Analytics</title>
  <meta name="description" content="Advanced analytics for educational performance prediction." />
  <meta name="theme-color" content={theme === "dark" ? "#141a18" : "#f6f7f5"} />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2" />
</svelte:head>

<div class="app-shell" class:dark={theme === "dark"}>
  <header class="topbar">
    <a class="brand" href="/" aria-label="GradePilot home">
      <img class="brand-mark" src="/favicon.svg?v=2" alt="" aria-hidden="true" />
      <span>GradePilot</span>
    </a>
    <div class="header-actions">
      <span class="model-status"><i></i>Model ready</span>
      <button class="theme-button" type="button" onclick={toggleTheme} aria-label={theme === "light" ? "Switch to dark theme" : "Switch to light theme"} title={theme === "light" ? "Switch to dark theme" : "Switch to light theme"}>
        {#if theme === "light"}<Moon size={18} />{:else}<Sun size={18} />{/if}
      </button>
    </div>
  </header>

  <main class="page-wrap">
    <section class="page-heading">
      <div>
        <p class="eyebrow">ADVANCED ANALYTICS</p>
        <h1>Advanced Analytics for Educational Performance Prediction</h1>
        <p class="page-description">Estimate a student's final grade from academic history, study habits, and learning context.</p>
      </div>
      <div class="dataset-meta"><span>RANDOM FOREST</span><span>31 predictors</span></div>
    </section>

    <section class="workspace-grid">
      <form class="profile-card" onsubmit={(event) => { event.preventDefault(); predict(); }}>
        <div class="panel-heading">
          <div><p class="eyebrow">STUDENT PROFILE</p><h2>Build a profile</h2></div>
          <button class="reset-button" type="button" onclick={resetForm}><RotateCcw size={16} />Reset sample</button>
        </div>
        <p class="panel-description">Change any field to explore a different student profile.</p>

        <div class="form-section">
          <h3><span>01</span> Student details</h3>
          <div class="field-grid">
            <label class="field"><span>Age</span><div class="select-wrap"><select bind:value={profile.age} aria-label="Age"><option value={15}>15 years</option><option value={16}>16 years</option><option value={17}>17 years</option><option value={18}>18 years</option><option value={19}>19 years</option><option value={20}>20 years</option><option value={21}>21 years</option><option value={22}>22 years</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Sex</span><div class="select-wrap"><select bind:value={profile.sex} aria-label="Sex"><option value="F">Female</option><option value="M">Male</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Family size</span><div class="select-wrap"><select bind:value={profile.famsize} aria-label="Family size"><option value="GT3">More than 3</option><option value="LE3">3 or fewer</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Mother's education</span><div class="select-wrap"><select bind:value={profile.Medu} aria-label="Mother's education"><option value={0}>None</option><option value={1}>Primary (grade 4)</option><option value={2}>5th–9th grade</option><option value={3}>Secondary</option><option value={4}>Higher education</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Father's education</span><div class="select-wrap"><select bind:value={profile.Fedu} aria-label="Father's education"><option value={0}>None</option><option value={1}>Primary (grade 4)</option><option value={2}>5th–9th grade</option><option value={3}>Secondary</option><option value={4}>Higher education</option></select><ChevronDown size={16} /></div></label>
          </div>
        </div>

        <div class="form-section">
          <h3><span>02</span> Learning &amp; wellbeing</h3>
          <div class="field-grid">
            <label class="field"><span>Weekly study time</span><div class="select-wrap"><select bind:value={profile.studytime} aria-label="Weekly study time"><option value={1}>Less than 2 hours</option><option value={2}>2–5 hours</option><option value={3}>5–10 hours</option><option value={4}>More than 10 hours</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Past class failures</span><div class="select-wrap"><select bind:value={profile.failures} aria-label="Past class failures"><option value={0}>None</option><option value={1}>1 class</option><option value={2}>2 classes</option><option value={3}>3 or more</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Plans for higher education</span><div class="select-wrap"><select bind:value={profile.higher} aria-label="Plans for higher education"><option value="yes">Yes</option><option value="no">No</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Internet access at home</span><div class="select-wrap"><select bind:value={profile.internet} aria-label="Internet access"><option value="yes">Yes</option><option value="no">No</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Family relationship</span><div class="select-wrap"><select bind:value={profile.famrel} aria-label="Family relationship"><option value={1}>Very difficult</option><option value={2}>Difficult</option><option value={3}>Neutral</option><option value={4}>Good</option><option value={5}>Very good</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Free time after school</span><div class="select-wrap"><select bind:value={profile.freetime} aria-label="Free time after school"><option value={1}>Very little</option><option value={2}>A little</option><option value={3}>Some</option><option value={4}>A lot</option><option value={5}>Very much</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Current health</span><div class="select-wrap"><select bind:value={profile.health} aria-label="Current health"><option value={1}>Very poor</option><option value={2}>Poor</option><option value={3}>Fair</option><option value={4}>Good</option><option value={5}>Very good</option></select><ChevronDown size={16} /></div></label>
            <label class="field"><span>Absences this year</span><input type="number" min="0" max="93" bind:value={profile.absences} aria-label="Absences this year" /></label>
          </div>
        </div>

        <div class="form-section grades-section">
          <h3><span>03</span> Recent grades <small>0–20 scale</small></h3>
          <div class="field-grid grade-grid">
            <label class="field"><span>Period 1 <b>G1</b></span><div class="number-wrap"><input type="number" min="0" max="20" bind:value={profile.G1} aria-label="Period 1 grade" /><span>/20</span></div></label>
            <label class="field"><span>Period 2 <b>G2</b></span><div class="number-wrap"><input type="number" min="0" max="20" bind:value={profile.G2} aria-label="Period 2 grade" /><span>/20</span></div></label>
          </div>
        </div>

        <div class="form-footer">
          <span><CircleHelp size={16} />Estimate for exploration, not a final assessment.</span>
          <button class="predict-button" type="submit" disabled={busy}>{#if busy}<LoaderCircle size={17} class="spin" />Analyzing{:else}Get outlook <ArrowRight size={17} />{/if}</button>
        </div>
      </form>

      <aside class="results-column" aria-live="polite">
        <section class="result-card">
          <div class="panel-heading result-heading"><div><p class="eyebrow">MODEL OUTLOOK</p><h2>Prediction</h2></div><span class="model-status"><i></i>{prediction ? "Updated" : "Ready"}</span></div>
          {#if prediction}
            <div class="outcome-banner" class:positive={isPass} class:negative={!isPass}>
              <div><span>FINAL GRADE OUTLOOK</span><h3>PREDICTED: {prediction.pass_fail}</h3><p>{isPass ? "The estimated grade meets the passing mark." : "The estimated grade is below the passing mark; early support may help."}</p></div>
              <span class="outcome-pill">{prediction.pass_fail}</span>
            </div>
            <div class="metric-grid">
              <div class="metric"><span>Estimated final grade</span><strong>{prediction.predicted_grade.toFixed(1)}<small>/20</small></strong><em>{prediction.percentage}</em></div>
              <div class="metric"><span>Passing mark</span><strong>10<small>/20</small></strong><em>50% required to pass</em></div>
            </div>
            <p class="grade-note"><CircleHelp size={16} />The grade is predicted directly from historical final-grade data. PASS means an estimate of 10/20 or higher. Use this as an early-support estimate, not a final assessment.</p>
            <div class="insight-heading"><h3>Why this result?</h3><span>Profile signals</span></div>
            {#each insights() as item}
              <div class="insight-row"><span class="insight-icon" class:watch={!item.positive}>{#if item.positive}<Check size={15} />{:else}<span>!</span>{/if}</span><div><strong>{item.title}</strong><p>{item.note}</p></div></div>
            {:else}
              <p class="no-insights">No standout signals in these fields. Try adjusting one or two values.</p>
            {/each}
            <div class="insight-heading recommendation-title"><h3>Recommendations</h3><span>Suggested next steps</span></div>
            <div class="recommendation-list">
              {#each recommendations() as suggestion, index}
                <div class="recommendation"><strong><Sparkles size={14} /> Step {index + 1}</strong><p>{suggestion}</p></div>
              {/each}
            </div>
          {:else}
            <div class="empty-state"><span class="empty-icon"><Sparkles size={21} /></span><h3>Your outlook will appear here</h3><p>Adjust the student profile, then select <strong>Get outlook</strong>.</p></div>
          {/if}
          {#if errorMessage}<div class="error-message"><strong>Prediction unavailable</strong><p>{errorMessage}</p></div>{/if}
        </section>
        <p class="model-footnote">Random Forest grade regression · Combined Mathematics and Portuguese student data. School is excluded as a predictor.</p>
      </aside>
    </section>
    <footer class="page-footer">GradePilot <span>·</span> Advanced Analytics for Educational Performance Prediction</footer>
  </main>
</div>
