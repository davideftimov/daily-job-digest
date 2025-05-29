let jobsContainer, loadingMessage, errorMessage, jobsCount, currentDate, currentDateElement;
let currentSource = 'all';

function displayJobs(jobs) {
    const filteredJobs = jobs.filter(job => job.filter === true && !job.viewed);
    jobsCount.textContent = `${filteredJobs.length} ${filteredJobs.length === 1 ? 'job' : 'jobs'}`;
    jobsCount.classList.remove('hidden');

    // Separate jobs with and without companies
    const standAloneJobs = filteredJobs.filter(job => !job.company);
    const jobsWithCompany = filteredJobs.filter(job => job.company);

    // Group jobs by company
    const jobsByCompany = jobsWithCompany.reduce((acc, job) => {
        if (!acc[job.company]) acc[job.company] = [];
        acc[job.company].push(job);
        return acc;
    }, {});

    // Display company groups
    Object.entries(jobsByCompany).forEach(([company, companyJobs]) => {
        const groupDiv = document.createElement('div');
        groupDiv.className = "job-group relative mb-8";

        const jobsWrapper = document.createElement('div');
        jobsWrapper.className = "jobs-wrapper relative";

        if (companyJobs.length > 1) {
            const peekLeft = document.createElement('div');
            peekLeft.className = "peek-left";
            peekLeft.onclick = (e) => {
                e.stopPropagation();
                navigateJobs(groupDiv, 'prev');
            };
            peekLeft.style.display = 'none';
            jobsWrapper.appendChild(peekLeft);

            const peekRight = document.createElement('div');
            peekRight.className = "peek-right";
            peekRight.onclick = (e) => {
                e.stopPropagation();
                navigateJobs(groupDiv, 'next');
            };
            jobsWrapper.appendChild(peekRight);
        }

        companyJobs.forEach((job, index) => {
            const jobDiv = document.createElement('div');
            jobDiv.className = `job-card rounded-lg p-4 border border-slate-800 shadow-md
    ${index === 0 ? 'block' : 'hidden'} relative`;
            jobDiv.dataset.index = index;
            jobDiv.dataset.total = companyJobs.length;

            jobDiv.innerHTML = job.source === 'hackernews'
                ? getHackerNewsTemplate(job)
                : getDefaultJobTemplate(job);

            jobsWrapper.appendChild(jobDiv);
        });

        if (companyJobs.length > 1) {
            const indicators = document.createElement('div');
            indicators.className = "flex justify-center gap-2 my-2";
            companyJobs.forEach((_, idx) => {
                const dot = document.createElement('div');
                dot.className = `h-2 w-2 rounded-full transition-colors duration-300
          ${idx === 0 ? 'bg-zinc-300' : 'bg-zinc-700'}`;
                dot.onclick = () => navigateToJob(groupDiv, idx);
                indicators.appendChild(dot);
            });
            groupDiv.appendChild(indicators);
        }

        groupDiv.appendChild(jobsWrapper);
        jobsContainer.appendChild(groupDiv);
    });

    // Display standalone jobs
    standAloneJobs.forEach(job => {
        const groupDiv = document.createElement('div');
        groupDiv.className = "job-group relative mb-8";

        const jobsWrapper = document.createElement('div');
        jobsWrapper.className = "jobs-wrapper relative";

        const jobDiv = document.createElement('div');
        jobDiv.className = "job-card rounded-lg p-4 border border-slate-800 shadow-md block relative";
        jobDiv.dataset.index = "0";
        jobDiv.dataset.total = "1";

        jobDiv.innerHTML = job.source === 'hackernews'
            ? getHackerNewsTemplate(job)
            : getDefaultJobTemplate(job);

        jobsWrapper.appendChild(jobDiv);
        groupDiv.appendChild(jobsWrapper);
        jobsContainer.appendChild(groupDiv);
    });
}

function getHackerNewsTemplate(job) {
    const hnDate = new Date(job.time * 1000).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
    return `
<div class="flex justify-between">
  <p class="text-sm text-end">${hnDate}</p>
  <a href="${job.url}"
    class="text-blue-500 hover:underline view-link"
    target="_blank" rel="noopener noreferrer"
    data-job-id="${job.id}">
    View on Hacker News
  </a>
</div>
<div class="flex justify-end">
  <p class="cursor-pointer text-blue-500 hide-link" data-job-id="${job.id}">Hide</p>
</div>
<hr class="my-4 border-slate-800">
<div class="mt-2">${job.text}</div>
`;
}

function getDefaultJobTemplate(job) {
    const defaultDate = new Date(job.time * 1000).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
    const jobText = `<div class="markdown-body">${marked.parse(job.text)}</div>`;
    return `
<div class="flex justify-between">
  <p class="font-bold">${job.title}</p>
  <a href="${job.url}"
    class="text-blue-500 hover:text-blue-700 view-link"
    target="_blank" rel="noopener noreferrer"
    data-job-id="${job.id}">
    View on ${job.source.charAt(0).toUpperCase() + job.source.slice(1)}
  </a>
</div>
<div class="flex justify-between">
  <p class="">${job.company}</p>
  <p class="cursor-pointer text-blue-500 hover:text-blue-700 hide-link" data-job-id="${job.id}">Hide</p>
</div>
<div class="flex justify-between">
  <p class="text-sm text-end">${defaultDate}</p>
  <p class="text-sm">${job.location}</p>
</div>
<hr class="my-4 border-slate-800">
<div class="mt-2">${jobText}</div>
`;
}

function navigateJobs(groupDiv, direction) {
    const cards = groupDiv.querySelectorAll('.job-card');
    const currentCard = groupDiv.querySelector('.job-card:not(.hidden)');
    const currentIndex = parseInt(currentCard.dataset.index);
    const totalCards = parseInt(currentCard.dataset.total);

    let nextIndex = direction === 'next'
        ? (currentIndex + 1) % totalCards
        : (currentIndex - 1 + totalCards) % totalCards;

    updateActiveCard(groupDiv, nextIndex);
}

function navigateToJob(groupDiv, index) {
    updateActiveCard(groupDiv, index);
}

function updateActiveCard(groupDiv, newIndex) {
    const cards = groupDiv.querySelectorAll('.job-card');
    const indicators = groupDiv.querySelectorAll('.rounded-full');
    const leftPeek = groupDiv.querySelector('.peek-left');
    const rightPeek = groupDiv.querySelector('.peek-right');
    const totalCards = cards.length;

    // Show/hide cards
    cards.forEach((card, idx) => {
        card.classList.toggle('hidden', idx !== newIndex);
    });

    // Update indicators
    indicators.forEach((dot, idx) => {
        dot.classList.toggle('bg-zinc-300', idx === newIndex);
        dot.classList.toggle('bg-zinc-700', idx !== newIndex);
    });

    // Show/hide peeks based on available posts
    if (leftPeek) {
        leftPeek.style.display = newIndex === 0 ? 'none' : 'block';
    }
    if (rightPeek) {
        rightPeek.style.display = newIndex === totalCards - 1 ? 'none' : 'block';
    }
}

async function fetchJobs(restoreScroll = false) {
    const scrollPosition = restoreScroll ? window.scrollY : 0;

    try {
        clearJobs();
        loadingMessage.classList.remove('hidden');
        errorMessage.classList.add('hidden');

        const dateStr = formatDateForAPI(currentDate);
        currentDateElement.textContent = formatDateForDisplay(currentDate);

        const params = new URLSearchParams({
            target_date: dateStr
        });

        if (currentSource !== 'all') {
            params.append('source', currentSource);
        }

        const response = await fetch(`http://127.0.0.1:8000/jobs/?${params}`);
        if (!response.ok) {
            throw new Error("Failed to fetch jobs");
        }
        const jobs = await response.json();
        displayJobs(jobs);

        if (restoreScroll) {
            window.scrollTo(0, scrollPosition);
        }
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.classList.remove('hidden');
    } finally {
        loadingMessage.classList.add('hidden');
    }
}

function formatDateForAPI(date) {
    return date.toLocaleDateString('en-CA');
}

function formatDateForDisplay(date) {
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
    });
}

function clearJobs() {
    while (jobsContainer.lastChild &&
        !['loading', 'error', 'jobs-count'].includes(jobsContainer.lastChild.id)) {
        jobsContainer.removeChild(jobsContainer.lastChild);
    }
}

async function markViewed(jobId, isHideAction = false) {
    try {
        await fetch(`http://127.0.0.1:8000/jobs/${jobId}/viewed`, {
            method: 'PUT'
        });
        console.log(`Job ${jobId} marked as viewed.`);

        // Remove the job from the DOM instead of refetching
        removeJobFromDOM(jobId);
    } catch (error) {
        console.error(`Failed to mark job ${jobId} as viewed.`, error);
    }
}

function removeJobFromDOM(jobId) {
    // Find the job card containing the clicked link
    const link = document.querySelector(`[data-job-id="${jobId}"]`);
    if (!link) return;

    // Navigate up to the job card
    const jobCard = link.closest('.job-card');
    if (!jobCard) return;

    // Get the job group container
    const jobGroup = jobCard.closest('.job-group');
    if (!jobGroup) return;

    const jobsWrapper = jobGroup.querySelector('.jobs-wrapper');
    const allCards = jobsWrapper.querySelectorAll('.job-card');
    const totalCards = allCards.length;
    const currentCardIndex = parseInt(jobCard.dataset.index);

    // Update job count
    updateJobCount(-1);

    // Handle differently based on whether this is a standalone job or part of a group
    if (totalCards === 1) {
        // If it's the only job in the group, remove the entire group
        jobGroup.remove();
    } else {
        // If part of a group with multiple jobs
        jobCard.remove();

        // Update indices for remaining cards
        const remainingCards = jobsWrapper.querySelectorAll('.job-card');
        remainingCards.forEach((card, idx) => {
            card.dataset.index = idx;
            card.dataset.total = totalCards - 1;
        });

        // Update indicators
        const indicators = jobGroup.querySelectorAll('.rounded-full');
        if (indicators.length > 0) {
            // Remove the indicator for the removed job
            if (indicators[currentCardIndex]) {
                indicators[currentCardIndex].remove();
            }

            // Update remaining indicators
            const remainingIndicators = jobGroup.querySelectorAll('.rounded-full');
            remainingIndicators.forEach((dot, idx) => {
                dot.classList.toggle('bg-zinc-300', idx === 0);
                dot.classList.toggle('bg-zinc-700', idx !== 0);
                dot.onclick = () => navigateToJob(jobGroup, idx);
            });
        }

        // Show the first remaining job if the active one was removed
        if (currentCardIndex === 0 && remainingCards.length > 0) {
            remainingCards[0].classList.remove('hidden');
        } else {
            // If a card other than the first was removed, navigate to the previous index
            const newActiveIndex = Math.min(currentCardIndex, remainingCards.length - 1);
            updateActiveCard(jobGroup, newActiveIndex);
        }

        // Update peek buttons visibility
        updatePeekButtonsVisibility(jobGroup);
    }
}

function updatePeekButtonsVisibility(jobGroup) {
    const cards = jobGroup.querySelectorAll('.job-card');
    if (cards.length <= 1) {
        // If only 1 or 0 cards left, hide both peek buttons
        const peekButtons = jobGroup.querySelectorAll('.peek-left, .peek-right');
        peekButtons.forEach(btn => btn.style.display = 'none');
        return;
    }

    // Find the active card
    const activeCard = jobGroup.querySelector('.job-card:not(.hidden)');
    if (!activeCard) return;

    const activeIndex = parseInt(activeCard.dataset.index);
    const totalCards = cards.length;

    // Update peek buttons
    const leftPeek = jobGroup.querySelector('.peek-left');
    const rightPeek = jobGroup.querySelector('.peek-right');

    if (leftPeek) leftPeek.style.display = activeIndex === 0 ? 'none' : 'block';
    if (rightPeek) rightPeek.style.display = activeIndex === totalCards - 1 ? 'none' : 'block';
}

function updateJobCount(delta) {
    const currentCount = parseInt(jobsCount.textContent.split(' ')[0]);
    const newCount = currentCount + delta;
    jobsCount.textContent = `${newCount} ${newCount === 1 ? 'job' : 'jobs'}`;
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize global variables
    jobsContainer = document.getElementById('jobs-container');
    loadingMessage = document.getElementById('loading');
    errorMessage = document.getElementById('error');
    jobsCount = document.getElementById('jobs-count');
    currentDate = new Date();
    currentDateElement = document.getElementById('current-date');

    // Add source filter handlers
    document.querySelectorAll('.source-filter').forEach(button => {
        button.addEventListener('click', () => {
            // Update active state
            document.querySelectorAll('.source-filter').forEach(btn => {
                btn.classList.remove('bg-slate-800');
            });
            button.classList.add('bg-slate-800');

            // Update source and fetch
            currentSource = button.dataset.source;
            fetchJobs();
        });
    });

    // Set initial active source
    document.querySelector('[data-source="all"]').classList.add('bg-slate-800');

    const prevDateBtn = document.getElementById('prev-date');
    const nextDateBtn = document.getElementById('next-date');

    // Event listeners and initialization
    prevDateBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 1);
        fetchJobs();
    });

    nextDateBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() + 1);
        fetchJobs();
    });

    // Add event delegation for view and hide links
    jobsContainer.addEventListener('click', async (e) => {
        if (e.target.classList.contains('view-link') || e.target.classList.contains('hide-link')) {
            const jobId = e.target.dataset.jobId;
            if (jobId) {
                await markViewed(jobId);
                e.preventDefault(); // Prevent navigation if it's a view link
            }
        }
    });

    // Update button state when date changes
    const observer = new MutationObserver(() => {
        const today = new Date();
        nextDateBtn.disabled = currentDate.getUTCDate() === today.getUTCDate();
        nextDateBtn.style.opacity = nextDateBtn.disabled ? '0.5' : '1';
    });
    observer.observe(currentDateElement, { childList: true });

    fetchJobs();
});