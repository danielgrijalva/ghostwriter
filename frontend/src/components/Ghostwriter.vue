<template>
  <div>
    <nav class="navbar navbar-dark bg-dark">
      <button class="navbar-toggler pull-xs-right" id="navbarSideButton" v-on:click="toggleOptions" type="button">
        &#9776;
      </button>      
      <a class="navbar-brand mx-auto" href="#"><h2 class="mb-1">Ghostwriter</h2></a>

      <ul class="navbar-side" id="navbarSide" v-bind:class="{ reveal: options }">
        <li class="navbar-side-item">
          <label for="topN">Number of suggestions ({{ topNShow }})</label>
          <input type="range" v-model.lazy="topN" v-model="topNShow" v-on:change="getSuggestions" class="custom-range" min="1" max="10" value="5" step="1">          
        </li>
        <hr class="separator">
        <li class="navbar-side-item">
          <label for="temp">Randomness ({{ tempShow }})</label>
          <input type="range" v-model.lazy="temp" v-model="tempShow" v-on:change="getSuggestions" class="custom-range" min="0" max="5" value="0" step=".1">          
        </li>
      </ul>
      <div class="overlay" v-if="options" v-on:click="toggleOptions"></div>      
    </nav>

    <div class="row">
      <div class="col suggestions">
        <div class="list-group" v-if="suggestions">
          <li class="list-group-item list-group-item-action" v-for="word in suggestions" v-on:click="buildStory(word)">
            {{ word }}
          </li>
          <li class="list-group-item customWord">
            <div class="input-group">
              <input id="customWord" @focus="toggleFocus" @blur="toggleFocus" type="text" class="form-control" v-model="customWord" placeholder="Other...">
            </div>
          </li>          
        </div>        
      </div>
      <div class="col"></div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Ghostwriter",
    data() {
      return {
        options: false,
        focused: false,
        nextWord: '',
        customWord: '',
        story: '',
        rawStory: '',
        suggestions: null,
        topN: 5,
        topNShow: 5,
        temp: 0,
        tempShow: 0,
      };
    },
    created: function (){
      var vm = this;
      this.getSuggestions();

      window.addEventListener('keydown', function(event) {
        if (event.keyCode == 8 && vm.story && vm.focused == false) { 
          vm.removeWord();
        }
      });
    },
    methods: {
      getSuggestions() {
        axios
          .get("http://127.0.0.1:8000/ghostwriter/", {
            params: {
              topN: this.topN,
              temp: this.temp,
              nextWord: this.nextWord,
              story: this.rawStory
            }
          })
          .then(response => (this.suggestions = response.data.suggestions));
      },
      buildStory(word){
        if (word != '<s>'){
          this.nextWord = word;
          // raw words and characters separated by spaces,
          // used by the algorithm to do inference
          this.rawStory = (this.rawStory + ' ' + word).trim();
          this.getSuggestions();

          // more human-readable story, for user presentation
          // capitalize first letter, trim spaces between symbols, etc
          this.formatStory();
        } else {
          // user selected META_TOKEN (<end> of string).
          // META_TOKEN usually gets suggested when the story should end.
          this.suggestions = null;
        }
      },
      formatStory(){
        this.story = this.rawStory[0].toUpperCase() + this.rawStory.substring(1);
      },
      removeWord(){
        var words = this.rawStory.split(' ');
        words.pop();

        if (words.length == 0) {
          this.reset();
        } else {
          this.rawStory = words.join(' ');
          this.formatStory();
        }

        this.getSuggestions();
      },
      reset(){
        this.nextWord = '';
        this.rawStory = '';
        this.story = '';
      },
      toggleOptions(){
        this.options = !this.options;
      },
      toggleFocus(){
        this.focused = !this.focused;
        console.log(this.focused)
      },
    }
  };
</script>