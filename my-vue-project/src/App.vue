<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">

  <div class="container mt-5">
    <!-- Input for uploading an image file -->
    <div class="row align-items-start p-3">
      <h4>sight scan</h4>
    </div>

    <div class="row align-items-start p-5">
      <p>Experience enhanced accessibility with our website! Easily upload or capture product descriptions. Our cutting-edge OCR technology extracts text, providing concise summaries. Ideal for visually impaired or elderly individuals struggling with small print, we empower users with audible descriptions for informed decision-making. </p>
    </div>

    <div class="row align-items-start p-3">
      <div class="col-6">
        <input type="file" @change="handleFileChange" accept="image/*" class="form-control mb-3">
        <img v-if="imageUrl" :src="imageUrl" alt="Uploaded Image" class="img-fluid mb-3">
        <div v-if="loading" class="spinner-border" role="status">
          <span class="sr-only"></span>
        </div>
      </div>
      <div class="col-6">
        <video ref="video" autoplay class="mb-3"></video>
        <button @click="captureImage" class="btn btn-primary mb-3">Take Picture</button>
      </div>
    </div>

    <div v-if="text">
      <div class="row align-items-start p-3">
        <div class="col-3">
          <h5>Extracted Text</h5><br>
          <p>{{ text }}</p>
        </div>
        <div class="col-9">
            <h5>Summary</h5><br>
            <button @click="speakSummary" class="btn btn-primary">Read Summary</button>
            <p>{{ summary }}</p>
        </div>
      </div>  
    </div>
    
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      text: '',
      summary: '',
      imageUrl:'',
      loading: false
    };
  },
  methods: {
    async handleFileChange(event) {
      const file = event.target.files[0];
      this.imageUrl = URL.createObjectURL(file);
      await this.processImage(file);
    },
    async captureImage() {
      try {
        const video = this.$refs.video;
        const constraints = {
          audio: false,
          video: true
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;

        // Wait for the video to load metadata
        await new Promise((resolve) => {
          video.onloadedmetadata = () => resolve();
        });

        // Pause the video to freeze the current frame
        video.pause();

        // Get the canvas element and draw the current video frame onto it
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert the canvas content to a blob
        canvas.toBlob(async (blob) => {
          // Process the captured image
          await this.processImage(blob);
        }, 'image/jpeg');
      } catch (error) {
        console.error('Error capturing image:', error);
      }
    },
    async processImage(fileOrBlob) {
      const formData = new FormData();
      formData.append('image', fileOrBlob);
      this.loading = true;

      try {
        const response = await axios.post('http://localhost:5001/extract_text', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.loading = false;
        this.text = response.data.text;
        this.summary = response.data.summary;
      } catch (error) {
        console.error('Error extracting text:', error);
      }
    }
  },
  speakSummary() {
      if (this.summary && this.synth) {
        // Split the summary into lines based on "-"
        const lines = this.summary.split('-');

        // Create an array to store each utterance
        const utterances = [];

        // Create an utterance for each line
        lines.forEach((line, index) => {
          // Trim leading and trailing whitespace
          const trimmedLine = line.trim();

          // Skip empty lines
          if (trimmedLine) {
            // Create an utterance for the line
            const utterance = new SpeechSynthesisUtterance(trimmedLine);

            // Add a delay before speaking subsequent lines to mimic line breaks
            if (index > 0) {
              utterance.onstart = () => {
                setTimeout(() => {
                  this.synth.speak(utterance);
                }, 500); // Adjust the delay as needed (in milliseconds)
              };
            }

            // Add the utterance to the array
            utterances.push(utterance);
          }
        });

        // Speak each utterance with a delay between them
        utterances.forEach((utterance, index) => {
          setTimeout(() => {
            this.synth.speak(utterance);
          }, index * 1000); // Adjust the delay between lines as needed (in milliseconds)
        });
      }
    }
}
</script>

<style>
#app {
  font-family: "Poppins", sans-serif;
  text-align: center;
}
.btn-primary {
  background-color: #C3B1E1;
}
</style>