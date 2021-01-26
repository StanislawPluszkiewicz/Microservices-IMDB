<template>
  <div id="app">
    <div id="header">
      <b-container>
      <b-row>
        <b-col cols="2">
          <router-link :to="{ name: 'Home' }">LOGO</router-link>
        </b-col>
        <b-col >
          <b-input-group>
            <b-form-input class="nav-search" placeholder="Search"></b-form-input>
            <b-button class="btn-search" variant="info"><v-icon name="search"/></b-button>
          </b-input-group>
        </b-col>
        <b-col cols="2">
          <b-dropdown text="Profile">
            <b-dropdown-item>Sign in</b-dropdown-item>
            <b-dropdown-item><b>Sign Up</b></b-dropdown-item>
          </b-dropdown>
        </b-col>
      </b-row>
      </b-container>
    </div>
    <router-view></router-view><!--Most important thing. Used to display components-->
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #d6d7d2;
  min-height: 100%;
}

#header {
  color: #ffffff;
  background-color: #17a2b8;
  padding-top: 15px;
  padding-bottom: 15px;
}

.nav-search {
  border: #ffffff;
  max-width: 700px;
}

.btn-search {
  color: #17a2b8;
  background-color: #ffffff;
  border: #ffffff;
  border-width: 1px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
}

.btn-search:hover {
  color: #ffffff;
  background-color: #e0e0e0;
  border: #e0e0e0;
  border-width: 1px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
}
</style>
