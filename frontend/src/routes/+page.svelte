<script lang="ts">
  import { ArrowRight, ArrowUpRight, BookOpen, Check, ChevronDown, CircleHelp, GraduationCap, LoaderCircle, RotateCcw, Sparkles, TrendingUp, Users } from "@lucide/svelte";

  type Profile = { age: number; sex: string; school: string; famsize: string; Medu: number; Fedu: number; studytime: number; failures: number; higher: string; internet: string; famrel: number; freetime: number; health: number; absences: number; G1: number; G2: number };
  type Prediction = { predicted_grade: number; percentage: string; pass_fail: "PASS" | "FAIL"; confidence: string; status: string };
  const defaults: Profile = { age: 17, sex: "F", school: "GP", famsize: "GT3", Medu: 3, Fedu: 2, studytime: 2, failures: 0, higher: "yes", internet: "yes", famrel: 4, freetime: 3, health: 3, absences: 4, G1: 12, G2: 13 };
  const modelDefaults = { address: "U", guardian: "mother", Mjob: "at_home", Fjob: "teacher", Pstatus: "T", reason: "course", activities: "no", schoolsup: "yes", nursery: "yes", traveltime: 2, paid: "no", famsup: "no", goout: 4, Walc: 1, romantic: "no", Dalc: 1 };
  let profile = $state<Profile>({ ...defaults });
  let prediction = $state<Prediction | null>(null);
  let busy = $state(false);
  let errorMessage = $state("");
  const pass = $derived(prediction?.pass_fail === "PASS");
  const confidenceValue = $derived(Number.parseFloat(prediction?.confidence ?? "0") || 0);
  const ringOffset = $derived(188.5 - (188.5 * confidenceValue) / 100);

  function resetForm() { profile = { ...defaults }; prediction = null; errorMessage = ""; }
  async function predict() {
    busy = true; errorMessage = ""; prediction = null;
    try {
      const response = await fetch("/api/predict", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ...profile, ...modelDefaults }) });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.detail ?? "The prediction service could not process this profile.");
      prediction = body as Prediction;
    } catch (error) { errorMessage = error instanceof Error ? error.message : "Unable to reach the prediction service. Please try again."; }
    finally { busy = false; }
  }
  function insights() {
    const items: { title: string; note: string; tone: string }[] = [];
    if (profile.G1 >= 15 || profile.G2 >= 15) items.push({ title: "Strong recent grades", note: "Recent marks point to a positive academic pattern.", tone: "good" });
    else if (profile.G1 < 10 || profile.G2 < 10) items.push({ title: "Recent grades need attention", note: "A check-in could uncover where coursework support is needed.", tone: "watch" });
    if (profile.studytime >= 3) items.push({ title: "A steady study routine", note: "Regular weekly study time can help sustain progress.", tone: "good" });
    if (profile.failures > 0) items.push({ title: "Past class challenges", note: `${profile.failures} previous failure(s) may be worth discussing.`, tone: "watch" });
    if (profile.absences > 10) items.push({ title: "Attendance may be a factor", note: `${profile.absences} absences could affect time in class.`, tone: "watch" });
    else if (profile.absences <= 5) items.push({ title: "Consistent attendance", note: "The reported absence count is relatively low.", tone: "good" });
    if (profile.Medu >= 3 || profile.Fedu >= 3) items.push({ title: "Learning support at home", note: "Build on the support and resources already available.", tone: "good" });
    return items.slice(0, 3);
  }
</script>

<svelte:head>
  <title>GradePilot — Student performance studio</title>
  <meta name="description" content="Explore student performance indicators with GradePilot's academic analytics studio." />
  <meta name="theme-color" content="#f4f3ed" />
</svelte:head>

<div class="app-shell">
  <aside class="sidebar">
    <a class="brand" href="/" aria-label="GradePilot home"><span class="brand-mark"><i></i><i></i><i></i><i></i></span><span class="brand-name">gradepilot<span>®</span></span></a>
    <div class="workspace-label">WORKSPACE</div>
    <nav class="side-nav" aria-label="Main navigation">
      <a href="#workspace" class="nav-item active"><span class="nav-dot"></span>Overview</a>
      <a href="#student-profile" class="nav-item"><Users size={17} strokeWidth={1.8} />Student profile</a>
      <a href="#model-note" class="nav-item"><BookOpen size={17} strokeWidth={1.8} />Model notes</a>
    </nav>
    <div class="sidebar-spacer"></div>
    <div class="sidebar-dataset"><div class="dataset-icon"><TrendingUp size={17} /></div><div><span class="dataset-eyebrow">CURRENT DATASET</span><strong>Student performance</strong><small>Portuguese schools · 2008</small></div><span class="dataset-live"></span></div>
    <div class="sidebar-footer"><span class="avatar">GP</span><span><strong>Academic insights</strong><small>Local workspace</small></span><CircleHelp size={16} /></div>
  </aside>

  <main id="workspace" class="main-content">
    <header class="topbar"><div class="breadcrumb"><span>Workspace</span><span class="crumb-slash">/</span><strong>Overview</strong></div><div class="topbar-right"><span class="model-status"><i></i>Model ready</span><span class="topbar-separator"></span><span class="model-tag">RF <i>·</i> v2.0</span></div></header>
    <div class="page-wrap">
      <section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="eyebrow-line"></span>ACADEMIC INTELLIGENCE <span class="eyebrow-year">/ 01</span></div><h1>See the story<br />behind <em>the score.</em></h1><p>A closer look at the factors shaping a student's academic outlook. Adjust the profile and explore what the model sees.</p><div class="hero-foot"><span class="hero-avatar-stack"><i>GP</i><i>RF</i><i>ML</i></span><span>Built for educators who look <strong>beyond the grade.</strong></span></div></div><div class="hero-art" aria-hidden="true"><div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div><div class="art-sun"></div><div class="art-arc arc-one"></div><div class="art-arc arc-two"></div><div class="art-star star-a">✳</div><div class="art-star star-b">✳</div><div class="art-coordinate">12° 34' 08" N<br />LEARNING IN MOTION</div><div class="art-caption"><span>01</span> STUDENT POTENTIAL</div></div></section>
      <section class="insight-strip" aria-label="Model summary"><div class="strip-item"><span class="strip-icon lime"><GraduationCap size={19} /></span><span><strong>Pass / fail outlook</strong><small>Binary classification model</small></span></div><div class="strip-rule"></div><div class="strip-item"><span class="strip-icon coral"><TrendingUp size={18} /></span><span><strong>32 student indicators</strong><small>Grades, habits &amp; context</small></span></div><div class="strip-rule"></div><div class="strip-item"><span class="strip-icon blue"><Sparkles size={18} /></span><span><strong>Built for exploration</strong><small>Change inputs, compare signals</small></span></div><a href="#model-note" class="strip-link" aria-label="Read model note"><ArrowUpRight size={17} /></a></section>
      <div class="section-heading" id="student-profile"><div><span class="section-kicker">STUDENT SNAPSHOT</span><h2>Shape a profile<span class="heading-period">.</span></h2></div><button class="reset-button" type="button" onclick={resetForm}><RotateCcw size={14} /> Reset to sample</button></div>

      <div class="workspace-grid">
        <form class="profile-card" onsubmit={(event) => { event.preventDefault(); predict(); }}>
          <div class="card-topline"><span>INPUT PROFILE</span><span class="step-count">01 <i>/</i> 02</span></div>
          <div class="form-intro"><div><h3>Student details</h3><p>Adjust the fields to explore a different profile.</p></div><span class="edit-glyph">✳</span></div>
          <div class="form-section-label"><span>01</span> STUDENT</div>
          <div class="field-grid">
            <label class="field"><span>Age</span><div class="select-wrap"><select bind:value={profile.age} aria-label="Age"><option value={15}>15 years</option><option value={16}>16 years</option><option value={17}>17 years</option><option value={18}>18 years</option><option value={19}>19 years</option><option value={20}>20 years</option><option value={21}>21 years</option><option value={22}>22 years</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Sex</span><div class="select-wrap"><select bind:value={profile.sex} aria-label="Sex"><option value="F">Female</option><option value="M">Male</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>School</span><div class="select-wrap"><select bind:value={profile.school} aria-label="School"><option value="GP">Gabriel Pereira (GP)</option><option value="MS">Mousinho da Silveira (MS)</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Family size</span><div class="select-wrap"><select bind:value={profile.famsize} aria-label="Family size"><option value="GT3">More than 3</option><option value="LE3">3 or fewer</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Mother's education <i>0—4</i></span><div class="select-wrap"><select bind:value={profile.Medu} aria-label="Mother's education"><option value={0}>None</option><option value={1}>Primary (grade 4)</option><option value={2}>5th–9th grade</option><option value={3}>Secondary</option><option value={4}>Higher education</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Father's education <i>0—4</i></span><div class="select-wrap"><select bind:value={profile.Fedu} aria-label="Father's education"><option value={0}>None</option><option value={1}>Primary (grade 4)</option><option value={2}>5th–9th grade</option><option value={3}>Secondary</option><option value={4}>Higher education</option></select><ChevronDown size={15} /></div></label>
          </div>
          <div class="form-section-label spaced"><span>02</span> LEARNING PATTERN</div>
          <div class="field-grid">
            <label class="field"><span>Weekly study time</span><div class="select-wrap"><select bind:value={profile.studytime} aria-label="Weekly study time"><option value={1}>Less than 2 hours</option><option value={2}>2–5 hours</option><option value={3}>5–10 hours</option><option value={4}>More than 10 hours</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Past class failures</span><div class="select-wrap"><select bind:value={profile.failures} aria-label="Past class failures"><option value={0}>None</option><option value={1}>1 class</option><option value={2}>2 classes</option><option value={3}>3 or more</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Plans for higher education</span><div class="select-wrap"><select bind:value={profile.higher} aria-label="Plans for higher education"><option value="yes">Yes</option><option value="no">No</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Internet access at home</span><div class="select-wrap"><select bind:value={profile.internet} aria-label="Internet access"><option value="yes">Yes</option><option value="no">No</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Family relationship <i>1—5</i></span><div class="select-wrap"><select bind:value={profile.famrel} aria-label="Family relationship"><option value={1}>Very difficult</option><option value={2}>Difficult</option><option value={3}>Neutral</option><option value={4}>Good</option><option value={5}>Very good</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Free time after school <i>1—5</i></span><div class="select-wrap"><select bind:value={profile.freetime} aria-label="Free time after school"><option value={1}>Very little</option><option value={2}>A little</option><option value={3}>Some</option><option value={4}>A lot</option><option value={5}>Very much</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Current health <i>1—5</i></span><div class="select-wrap"><select bind:value={profile.health} aria-label="Current health"><option value={1}>Very poor</option><option value={2}>Poor</option><option value={3}>Fair</option><option value={4}>Good</option><option value={5}>Very good</option></select><ChevronDown size={15} /></div></label>
            <label class="field"><span>Absences this year</span><input class="number-input" type="number" min="0" max="93" bind:value={profile.absences} aria-label="Absences this year" /></label>
          </div>
          <div class="form-section-label spaced"><span>03</span> RECENT GRADES <span class="grade-scale">0—20 SCALE</span></div>
          <div class="grade-fields"><label class="field"><span>Period 1 <i>G1</i></span><div class="grade-input"><input type="number" min="0" max="20" bind:value={profile.G1} aria-label="Period 1 grade" /><span>/20</span></div></label><label class="field"><span>Period 2 <i>G2</i></span><div class="grade-input"><input type="number" min="0" max="20" bind:value={profile.G2} aria-label="Period 2 grade" /><span>/20</span></div></label></div>
          <div class="form-footer"><span><CircleHelp size={14} />Inputs are used to explore a model estimate.</span><button class="predict-button" type="submit" disabled={busy}>{#if busy}<LoaderCircle size={16} class="spin" /> Analyzing{:else}Explore outlook <ArrowRight size={16} />{/if}</button></div>
        </form>

        <aside class="results-column" aria-live="polite">
          <section class:has-result={prediction} class:result-fail={prediction && !pass} class="result-card"><div class="result-card-pattern"></div><div class="result-topline"><span>MODEL OUTLOOK</span><span class="result-live"><i></i>{prediction ? "UPDATED JUST NOW" : "READY TO EXPLORE"}</span></div>
            {#if prediction}
              <div class="result-content"><div class="result-status" class:status-fail={!pass}><span class="status-mark">{#if pass}<Check size={13} />{:else}<span>!</span>{/if}</span>{pass ? "ON TRACK" : "SUPPORT MAY HELP"}</div><h3>{pass ? "Predicted to pass" : "At risk of not passing"}<span>.</span></h3><p class="result-subtitle">A snapshot of the model's outlook for this profile.</p>
                <div class="score-display"><div class="score-number"><span>ESTIMATED GRADE</span><div>{prediction.predicted_grade}<small>/20</small></div><strong>{prediction.percentage} <i>equivalent</i></strong></div><div class="confidence-ring" aria-label={`Model confidence ${prediction.confidence}`}><svg viewBox="0 0 72 72"><circle class="ring-track" cx="36" cy="36" r="30" /><circle class="ring-value" cx="36" cy="36" r="30" style={`stroke-dashoffset:${ringOffset}`} /></svg><div><strong>{prediction.confidence}</strong><small>confidence</small></div></div></div>
                <div class="outlook-scale"><div><span>0</span><span>PASS MARK · 10</span><span>20</span></div><div class="scale-track"><span class:fail-marker={!pass} style={`left:${Math.min(100, Math.max(0, prediction.predicted_grade * 5))}%`}></span><i></i></div></div><div class="estimate-note"><CircleHelp size={14} /><span>Grade is estimated from classifier confidence. The model predicts pass/fail; it does not independently predict a numeric grade.</span></div>
              </div>
            {:else}
              <div class="empty-result"><div class="empty-orbit"><div class="empty-orbit-inner"><Sparkles size={27} strokeWidth={1.5} /></div><i class="orbit-dot"></i><i class="orbit-dot second"></i></div><span class="empty-kicker">YOUR NEXT INSIGHT STARTS HERE</span><h3>Curiosity looks<br />good on you<span>.</span></h3><p>Set up a student profile, then see how the model reads the signals.</p><div class="empty-prompt"><span>01</span><span>Adjust any of the profile inputs</span><ArrowRight size={14} /></div><div class="empty-prompt"><span>02</span><span>Explore an academic outlook</span><ArrowRight size={14} /></div></div>
            {/if}
          </section>
          {#if errorMessage}<div class="error-card"><span class="error-icon">!</span><div><strong>Prediction unavailable</strong><p>{errorMessage}</p></div></div>{/if}
          {#if prediction}
            <section class="insights-card"><div class="mini-card-head"><div><span class="section-kicker">PROFILE READOUT</span><h3>What stands out<span>.</span></h3></div><span class="insight-count">{insights().length.toString().padStart(2, "0")}</span></div>{#each insights() as item}<div class="insight-row"><span class="insight-bullet" class:watch={item.tone === "watch"}>{#if item.tone === "good"}<Check size={13} />{:else}<span>!</span>{/if}</span><div><strong>{item.title}</strong><p>{item.note}</p></div></div>{:else}<p class="no-insights">No standout signals in these inputs. Try changing one or two fields and compare.</p>{/each}<div class="recommendation"><span class="recommendation-star">✳</span><p>{pass ? "Keep reinforcing the study and attendance habits that are working." : "Consider a supportive check-in and connecting the student with academic help."}</p></div></section>
          {:else}<section class="tip-card"><div class="tip-symbol">✳</div><div><span>GOOD TO KNOW</span><p>The model considers grades, study habits, attendance, family context and more.</p></div><ArrowUpRight size={16} /></section>{/if}
          <section class="model-note" id="model-note"><div class="note-heading"><span>THE MODEL, IN BRIEF</span><span class="note-index">02</span></div><div class="model-stat"><strong>90.5<span>%</span></strong><span>reported accuracy<br />in project materials</span></div><div class="note-divider"></div><p>Random Forest classifier trained on Portuguese secondary school records. This estimate is an exploratory signal, not a student's full story.</p><a href="#student-profile">Explore the inputs <ArrowRight size={14} /></a></section>
        </aside>
      </div>
      <footer class="page-footer"><span>GRADEPILOT <i>·</i> ACADEMIC ANALYTICS</span><span>AN EXPLORATORY TOOL <i>·</i> NOT A FINAL ASSESSMENT</span></footer>
    </div>
  </main>
</div>

