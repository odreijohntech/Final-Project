<script lang="ts">
  import { onMount } from "svelte";
  import { ArrowRight, Check, ChevronDown, CircleHelp, LoaderCircle, Moon, RotateCcw, Sparkles, Sun } from "@lucide/svelte";

  type Profile = { age: number; sex: string; school: string; famsize: string; Medu: number; Fedu: number; studytime: number; failures: number; higher: string; internet: string; famrel: number; freetime: number; health: number; absences: number; G1: number; G2: number };
  type Prediction = { predicted_grade: number; percentage: string; pass_fail: "PASS" | "FAIL"; confidence: string; status: string };
  const defaults: Profile = { age: 17, sex: "F", school: "GP", famsize: "GT3", Medu: 3, Fedu: 2, studytime: 2, failures: 0, higher: "yes", internet: "yes", famrel: 4, freetime: 3, health: 3, absences: 4, G1: 12, G2: 13 };
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
    if (profile.G1 >= 15 || profile.G2 >= 15) items.push({ title: "Strong recent grades", note: "Recent marks show a positive academic pattern.", positive: true });
    else if (profile.G1 < 10 || profile.G2 < 10) items.push({ title: "Recent grades need attention", note: "A check-in could identify where support is needed.", positive: false });
    if (profile.studytime >= 3) items.push({ title: "Regular study time", note: "A steady weekly routine can support progress.", positive: true });
    if (profile.failures > 0) items.push({ title: "Past class challenges", note: `${profile.failures} previous failure(s) may be worth discussing.`, positive: false });
    if (profile.absences > 10) items.push({ title: "Attendance may be a factor", note: `${profile.absences} absences could affect time in class.`, positive: false });
    else if (profile.absences <= 5) items.push({ title: "Consistent attendance", note: "The reported absence count is relatively low.", positive: true });
    if (profile.Medu >= 3 || profile.Fedu >= 3) items.push({ title: "Learning support at home", note: "Build on the support available to the student.", positive: true });
    return items.slice(0, 3);
  }
</script>

<svelte:head>
  <title>GradePilot — Student performance</title>
  <meta name="description" content="Explore student performance indicators with GradePilot." />
  <meta name="theme-color" content={theme === "dark" ? "#141a18" : "#f6f7f5"} />
</svelte:head>

<div class="app-shell" class:dark={theme === "dark"}>
  <header class="topbar">
    <a class="brand" href="/" aria-label="GradePilot home">
      <span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <span>GradePilot</span>
    </a>
    <div class="header-actions">
      <span class="model-status"><i></i>Model ready</span>
      <button class="theme-button" type="button" onclick={toggleTheme} aria-label={theme === "light" ? "Switch to dark theme" : "Switch to light theme"}>
        {#if theme === "light"}<Moon size={18} /> Dark mode{:else}<Sun size={18} /> Light mode{/if}
      </button>
    </div>
  </header>

  <main class="page-wrap">
    <section class="page-heading">
      <div>
        <p class="eyebrow">STUDENT PERFORMANCE</p>
        <h1>Understand the outlook.</h1>
        <p class="page-description">Explore how grades, study habits and student context shape the model's prediction.</p>
      </div>
      <div class="dataset-meta"><span>RANDOM FOREST</span><span>32 indicators</span></div>
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
            <label class="field"><span>School</span><div class="select-wrap"><select bind:value={profile.school} aria-label="School"><option value="GP">Gabriel Pereira (GP)</option><option value="MS">Mousinho da Silveira (MS)</option></select><ChevronDown size={16} /></div></label>
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
              <div><span>ESTIMATED RESULT</span><h3>{isPass ? "Predicted to pass" : "Support may help"}</h3></div>
              <span class="outcome-pill">{prediction.pass_fail}</span>
            </div>
            <div class="metric-grid">
              <div class="metric"><span>Estimated grade</span><strong>{prediction.predicted_grade}<small>/20</small></strong><em>{prediction.percentage}</em></div>
              <div class="metric"><span>Model confidence</span><strong>{prediction.confidence}</strong><em>for this outcome</em></div>
            </div>
            <p class="grade-note"><CircleHelp size={16} />The model predicts pass/fail. The displayed grade is estimated from its confidence.</p>
            <div class="insight-heading"><h3>What stands out?</h3><span>From this profile</span></div>
            {#each insights() as item}
              <div class="insight-row"><span class="insight-icon" class:watch={!item.positive}>{#if item.positive}<Check size={15} />{:else}<span>!</span>{/if}</span><div><strong>{item.title}</strong><p>{item.note}</p></div></div>
            {:else}
              <p class="no-insights">No standout signals in these fields. Try adjusting one or two values.</p>
            {/each}
            <div class="recommendation"><strong>Suggested next step</strong><p>{isPass ? "Keep supporting the study and attendance habits that are working." : "Consider a supportive check-in and additional academic help."}</p></div>
          {:else}
            <div class="empty-state"><span class="empty-icon"><Sparkles size={21} /></span><h3>Your outlook will appear here</h3><p>Adjust the student profile, then select <strong>Get outlook</strong>.</p></div>
          {/if}
          {#if errorMessage}<div class="error-message"><strong>Prediction unavailable</strong><p>{errorMessage}</p></div>{/if}
        </section>
        <p class="model-footnote">Random Forest classifier · Portuguese secondary school data</p>
      </aside>
    </section>
    <footer class="page-footer">GradePilot <span>·</span> Student performance insights</footer>
  </main>
</div>
