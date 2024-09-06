async function downloadYTVideo(url, default_filename, itag, last_audio){
    await eel.downloadVideo(url, default_filename, itag, last_audio)(async function(outfile){
        document.querySelector("#yt_loading").style.display = "block";
        if (outfile){
            document.querySelector('#yt_success_message').innerHTML = `<YouTube Video Downloading at : <br/>${outfile}`;
            //$('#result_section').html('');
            document.querySelector('#yt_url').value = '';
        }else{
            document.querySelector('#yt_error_message').innerText = 'Error Observered...';
        }

        setTimeout(() => {  document.querySelector("#yt_loading").style.display = "none"; }, 1000);
    })
}

document.querySelector('#yt_btn').addEventListener('click', async function(){
    var yt_url = document.querySelector('#yt_url');
    document.querySelector("#yt_loading").style.display = "block";
    document.querySelector("#yt_video_title").innerText = '';
    document.querySelector('#yt_error_message').innerText = '';
    document.querySelector('#yt_success_message').innerHTML = '';
    document.querySelector('#result_section').innerHTML = '';

    if (yt_url.value !== '' && isUrlValid1(yt_url.value)){
    
        await eel.searchURL(yt_url.value)(async function(result){

            if (result.error){
                document.querySelector('#yt_error_message').innerText = result.error;
                return
            }

        if (result){
            //$('#yt_form').hide();
            document.querySelector('#yt_video_title').innerText = result.full[0].title;

            var rowTable = `<div class="w3-section"><img src="${result.preview}" width="100%" /></div>
                            <div class=""><table class="w3-table-all"><thead>`;
            console.log(result);
            for (var x=0; x<result.video.length; x++){
                rowTable += `<tr style="cursor:pointer;font-size:10px;" onclick="downloadYTVideo('${yt_url.value}', '${result.video[x].default_filename}', '${result.video[x].itag}', '${result.last_audio}')"><th>${result.video[x].mime_type}</th><th>${result.video[x].filesize_mb} MB</th><th>${result.video[x].res} | ${result.video[x].fps} FPS | ${result.video[x].abr ? result.video[x].abr : '🔇'}</th></tr>`
            }

            for (var x=0; x<result.audio.length; x++){
                rowTable += `<tr style="cursor:pointer;font-size:10px;" onclick="downloadYTVideo('${yt_url.value}', '${result.audio[x].default_filename}', '${result.audio[x].itag}', '${result.last_audio}')"><th>${result.audio[x].mime_type}</th><th>${result.audio[x].filesize_mb} Mb</th><th>${result.audio[x].audio_codec} | ${result.audio[x].abr}</th></tr>`
            }

            rowTable += '</thead></table></div>';

            document.querySelector('#result_section').innerHTML = rowTable;
            }else{
                document.querySelector('#yt_error_message').innerText = 'No Result from Server....';
            }
                                     
        });
    }else{
        document.querySelector('#yt_error_message').innerText = 'No YouTube Link';
    }

    setTimeout(() => {  document.querySelector("#yt_loading").style.display = "none"; }, 1000);

})



document.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {  document.querySelector("#yt_loading").style.display = "none"; }, 1000);
})


function isUrlValid(url){
    try { return Boolean(new URL(url)); }
    catch(e){ return false; }
}


function isUrlValid1(url) {
    if(!url) return false;
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))|' + // OR ip (v4) address
        'localhost' + // OR localhost
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
    return pattern.test(url);
}