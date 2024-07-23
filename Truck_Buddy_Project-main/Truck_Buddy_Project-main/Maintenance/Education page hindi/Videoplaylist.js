const videosList = [
{
    video:'media/vid1.mp4',
    title:'ट्रक के महत्वपूर्ण भाग'
},
{
    video:'media/vid2.mp4',
    title:'ट्रक रखरखाव का महत्व'
},
{
    video:'media/vid3.mp4',
    title:'इंजन का रखरखाव'
},
{
    video:'media/vid4.mp4',
    title:'ब्रेक का रखरखाव'
},
]

const categories = [...new Set(videosList.map((item) => item.category))]; // Assuming each item has a 'category' property
document.getElementById('videosList').innerHTML = videosList.map((item) => {
    var { video, title } = item;
    return (
        `<div class="list active">
            <video src="${video}" class="list-video" controls></video>
            <h3 class="list-title">${title}</h3>
        </div>`
    );
}).join('');

// Select all the video list items
let videoList = document.querySelectorAll('.video-list-container .list');

// Function to update the main video player
function updateMainVideo(vid) {
    // Remove the 'active' class from all video list items
    videoList.forEach(item => item.classList.remove('active'));
    
    // Add the 'active' class to the clicked video list item
    vid.classList.add('active');
    
    // Get the source and title of the clicked video
    let src = vid.querySelector('.list-video').src;
    let title = vid.querySelector('.list-title').innerHTML;
    
    // Update the main video source and play the video
    let mainVideo = document.querySelector('.main-video-container .main-video');
    mainVideo.src = src;
    mainVideo.play();
    
    // Update the main video title
    document.querySelector('.main-video-container .main-title').innerHTML = title;
}

// Add click event listeners to each video list item
videoList.forEach(vid => {
    vid.addEventListener('click', () => updateMainVideo(vid));
});


