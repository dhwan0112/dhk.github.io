// Content Loader for Research Results
async function loadResearchResults() {
    try {
        const response = await fetch('content/research-results.json');
        const data = await response.json();

        // Load images
        if (data.images && data.images.length > 0) {
            const imageContainer = document.getElementById('image-gallery-grid');
            if (imageContainer) {
                imageContainer.innerHTML = data.images.map(item => `
                    <div class="gallery-item">
                        <div class="gallery-image">
                            ${item.imageUrl ?
                                `<img src="${item.imageUrl}" alt="${item.title}" style="width: 100%; height: 100%; object-fit: cover;">` :
                                `<div class="placeholder-gallery">
                                    <i class="fas fa-image"></i>
                                    <p>Image Placeholder</p>
                                </div>`
                            }
                        </div>
                        <div class="gallery-info">
                            <h3>${item.title}</h3>
                            <p>${item.description}</p>
                            <span class="gallery-date">Date: ${item.date}</span>
                        </div>
                    </div>
                `).join('');
            }
        }

        // Load videos
        if (data.videos && data.videos.length > 0) {
            const videoContainer = document.getElementById('video-gallery-grid');
            if (videoContainer) {
                videoContainer.innerHTML = data.videos.map(item => `
                    <div class="video-item">
                        <div class="video-wrapper">
                            ${item.videoUrl ?
                                (item.videoType === 'youtube' ?
                                    `<iframe src="${item.videoUrl}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width: 100%; height: 100%;"></iframe>` :
                                    `<video controls style="width: 100%; height: 100%;">
                                        <source src="${item.videoUrl}" type="video/mp4">
                                        Your browser does not support the video tag.
                                    </video>`
                                ) :
                                `<div class="placeholder-video">
                                    <i class="fas fa-video"></i>
                                    <p>Video Placeholder</p>
                                </div>`
                            }
                        </div>
                        <div class="video-info">
                            <h3>${item.title}</h3>
                            <p>${item.description}</p>
                            <span class="video-date">Date: ${item.date}</span>
                        </div>
                    </div>
                `).join('');
            }
        }

        // Load visualizations
        if (data.visualizations && data.visualizations.length > 0) {
            const vizContainer = document.getElementById('viz-grid');
            if (vizContainer) {
                vizContainer.innerHTML = data.visualizations.map(item => `
                    <div class="viz-item">
                        <div class="viz-preview">
                            ${item.imageUrl ?
                                `<img src="${item.imageUrl}" alt="${item.title}" style="width: 100%; height: 100%; object-fit: cover;">` :
                                `<div class="placeholder-viz">
                                    <i class="fas fa-chart-line"></i>
                                    <p>Visualization Placeholder</p>
                                </div>`
                            }
                        </div>
                        <div class="viz-info">
                            <h3>${item.title}</h3>
                            <p>${item.description}</p>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Error loading research results:', error);
    }
}

// Content Loader for Research Notes
async function loadResearchNotes() {
    try {
        const response = await fetch('content/research-notes.json');
        const data = await response.json();

        if (data.notes && data.notes.length > 0) {
            const notesContainer = document.getElementById('notes-container');
            if (notesContainer) {
                notesContainer.innerHTML = data.notes.map(note => `
                    <article class="note-entry">
                        <div class="note-header">
                            <h2 class="note-title">${note.title}</h2>
                            <div class="note-meta">
                                <span class="note-date"><i class="far fa-calendar"></i> ${note.date}</span>
                                <span class="note-category"><i class="fas fa-tag"></i> ${note.category}</span>
                            </div>
                        </div>
                        <div class="note-content">
                            <h3>Objective</h3>
                            <p>${note.objective}</p>

                            <h3>Procedure</h3>
                            <ol>
                                ${note.procedure.map(step => `<li>${step}</li>`).join('')}
                            </ol>

                            <h3>Observations</h3>
                            <p>${note.observations}</p>

                            <h3>Data</h3>
                            <p>${note.data}</p>

                            <h3>Conclusions</h3>
                            <p>${note.conclusions}</p>

                            ${note.attachments && note.attachments.length > 0 ? `
                                <div class="note-attachments">
                                    <h4>Attachments:</h4>
                                    <div class="attachment-list">
                                        ${note.attachments.map(att => `
                                            <span class="attachment-item">
                                                <i class="fas fa-file-${att.type}"></i> ${att.name}
                                            </span>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    </article>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Error loading research notes:', error);
    }
}

// Initialize content loading based on current page
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();

    if (currentPage === 'research-results.html') {
        loadResearchResults();
    } else if (currentPage === 'research-notes.html') {
        loadResearchNotes();
    }
});
