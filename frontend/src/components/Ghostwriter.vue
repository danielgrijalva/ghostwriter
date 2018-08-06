<template>
  <div id="wrapper" v-bind:class="{ toggled: options }">
    <div id="page-content-wrapper">
      <div class="row ghostwriter">        
        <div class="" id="toggleOptions">
          <button class="btn btn-lg btn-link toggleOptions" v-on:click="toggleOptions">
            <i class="fas fa-cog"></i>
          </button>
        </div>

        <div class="col text-center">
          <img class="img-fluid" width="200px" src="../assets/logo.png">
          <h1>Ghostwriter</h1>

          <!-- suggestions -->
          <div class="suggestions-container" v-if="suggestions">
            <div class="suggestions-results" aria-labelledby="autosuggest">
              <ul role="listbox" aria-labelledby="autosuggest">
                <li v-for="word in suggestions" v-on:click="buildStory(word)" class="suggestions-results-item">
                  {{ word }}
                </li>
                <li>
                  <div class="input-group m-2"  style="max-width: 97%;">
                    <input @focus="toggleFocus" @blur="toggleFocus" type="text" class="form-control" v-model="customWord" placeholder="Other...">
                    <div class="input-group-append">
                      <button class="btn btn-outline-gray" type="button" v-on:click="buildStory(customWord)" id="button-addon2"><i class="fas fa-angle-right"></i></button>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
           
          <div class="story">
            <h3 v-model="story" class="text-left p-5">
              {{ story }}
            </h3> 
          </div>
        </div>
      </div>
    </div>


    <div id="sidebar-wrapper">
      <ul class="sidebar-nav">
        <li>
          <label for="topN">Number of suggestions ({{ topNShow }})</label>
          <input type="range" v-model.lazy="topN" v-model="topNShow" v-on:change="getSuggestions" class="custom-range" min="1" max="10" value="5" step="1">          
        </li>
        <hr>
        <li>
          <label for="temp">Randomness ({{ tempShow }})</label>
          <input type="range" v-model.lazy="temp" v-model="tempShow" v-on:change="getSuggestions" class="custom-range" min="0" max="5" value="0" step=".1">          
        </li>        
      </ul>       
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