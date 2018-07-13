<template>
  <div class="hello">
    <h1>Ghostwriter</h1>
    <div class="form-group">
      <textarea class="form-control" id="story" rows="3" v-model="story" @input="toUpper"></textarea>
      <br>
      <p>
        {{ upperStory }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Ghostwriter",
  data() {
    return {
      story: null,
      upperStory: null,
    };
  },
  mounted() {
    this.toUpper();
  },
  methods: {
    toUpper() {
      axios
        .get("http://127.0.0.1:8000/upper/", {
          params: {
            text: this.story
          }
        })
        .then(response => (this.upperStory = response.data.result));
    }
  }
};
</script>
