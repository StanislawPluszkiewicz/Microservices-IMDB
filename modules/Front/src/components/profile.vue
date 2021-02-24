<template>
<b-container>
    <div>
        <b-row>
            <h1><b>Profile of {{ this.$parent.user.firstname }} {{ this.$parent.user.lastname }}</b></h1>
        </b-row>
        <b-row>
            <p><b>Username: </b> {{ this.$parent.user.username }}</p>
        </b-row>
        <b-row>
            <p><b>Email: </b>{{ this.$parent.user.mail }}</p>
        </b-row>
    </div>
    <div class="comment-list">
      <b-container v-if="comments.length > 0">
        <b-row>
          <h4>Your comments</h4>
        </b-row>
        <b-row class="comment" v-for="(comment, index) in comments" :key='`tag-${index}`'>
          <b-container>
            <b-row class="comment-header">
              <b-col cols="2" class="title">
                <b>For {{comment.movieName}}</b>
              </b-col>
              <b-col cols="3" class="title">
                {{parseDate(comment.date)}}
              </b-col>
              <b-col cols="1" class="title">
                {{comment.note}}<v-icon style="color: gold;" name="star"/>
              </b-col>
            </b-row>
            <b-row class="comment-review">
              {{comment.review}}
            </b-row>
          </b-container>
        </b-row>
      </b-container>
      <b-container v-else>
        <b-row>
          <h4>You haven't commented on any movie yet</h4>
        </b-row>
      </b-container>
    </div>
</b-container>
</template>
<script>
export default {
name: "profile",
  data: function() {
    return {
      comments: [],
      id: '',

    }
  },
  watch: {
    '$route': 'fetchData'
  },
  created: function() {
    this.fetchData()
  },
  methods:{
    fetchData: function() {
      console.log("Fetch data")
      var that = this
      that.loading = false
      //console.log(this.$route.params.id)
      this.id = this.$route.params.id

      this.$axios
      .get('http://127.0.0.1:5005/comments?userID='+ this.id)
      .then(res => {
        console.log(res)
        that.comments = res.data.data.comments
      })
      .catch(error => console.log(error))
      .finally(function(){
        that.loading = false
      });
    },
    parseDate: function (oldDate) {
        return oldDate.slice(4)
    }
  }
}
</script>
<style>

#comments
{
  text-align: left;
  margin-top: 3%;
}

.title{
  padding: 0px;
  text-align: left;
}

.comment-editor{
  margin-top: 5%;
}

.comment-btn{
  width: 75px;
  margin-top: 2%;
  
}

.comment-list{
  margin-top: 5%;
}

.comment{
  margin-top: 3%;
  margin-bottom: 3%;
  border: solid 2px;
  border-color: #17a2b8;
}

.comment{
  padding: 20px;
  margin-top: 3%;
  margin-bottom: 3%;
  border: solid 2px;
  border-color: #17a2b8;
  border-radius: 10px;
  background-color: #f7f7f7;
}

.comment-header{
  padding-bottom: 2%;
}

.comment-review{
  text-align:left;
}
</style>