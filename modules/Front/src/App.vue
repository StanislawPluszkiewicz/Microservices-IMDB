<template>
  <div id="app">
    <div id="header">
      <b-container>
      <b-row>
        <b-col cols="2">
          <img src="src/assets/logo_mmdb.png" width="150px" height="50px" v-on:click="goHomePage()"/>
        </b-col>
        <b-col>
          <b-input-group>
            <b-form-input v-model="search" class="nav-search" placeholder="Search"></b-form-input>
            <b-button class="btn-search" @click="goHomePage()"><v-icon name="search"/></b-button>
          </b-input-group>
        </b-col>
        <b-col cols="2">
          <b-dropdown :text="this.isConnected ? this.user.username : 'Profile'">
            <div v-if="this.isConnected === false">
              <b-dropdown-item @click="showModalSignIn()">Sign in</b-dropdown-item>
              <b-dropdown-item @click="showModalSignUp()"><b>Sign Up</b></b-dropdown-item>
            </div>
            <div v-if="this.isConnected === true">
              <b-dropdown-item @click="goToProfile()">Go to profile</b-dropdown-item>
              <b-dropdown-item @click="logout()"><b>Log out</b></b-dropdown-item>
            </div>
          </b-dropdown>
          <div>
              <b-modal hide-footer ref="modal-loading" title="Accessing the internet...">
                <div style="padding: 15px; text-align:center;"><img src="src/assets/spinner.gif" width="50px" height="50px"/></div>
              </b-modal>
              <b-modal
                ref="modal-signin"
                title="Sign In"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOkIn">
                  <b-form ref="form" @submit.prevent="submitSignIn">
                    <b-form-group 
                    label-for="signin-input"
                    :state="nameState"
                    invalid-feedback="Name is required">
                      <p>Username</p>
                      <b-form-input
                        id="name-input"
                        v-model="user.username"
                        :state="nameState"
                        required
                      ></b-form-input>
                      <p>Password</p>
                      <b-form-input
                        v-model="user.password"
                        :state="nameState"
                        required
                        type="password"
                      ></b-form-input>
                    </b-form-group>
                  </b-form>
              </b-modal>
              <b-modal
                ref="modal-signup"
                title="Sign Up"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOkUp">
                  <form ref="form" @submit.stop.prevent="submitSignUp">
                    <b-form-group
                      label-for="signup-input">
                      <p>Username</p>
                      <b-form-input
                        v-model="registerUser.username"
                        required
                      ></b-form-input>
                      <p>Password</p>
                      <b-form-input
                        v-model="registerUser.password"
                        required
                        type="password"
                      ></b-form-input>
                      <p>Email</p>
                      <b-form-input
                        v-model="registerUser.mail"
                        required
                      ></b-form-input>
                      <p>Firstname</p>
                      <b-form-input
                        v-model="registerUser.firstname"
                        required
                      ></b-form-input>
                      <p>Lastname</p>
                      <b-form-input
                        v-model="registerUser.lastname"
                        required
                      ></b-form-input>
                    </b-form-group>
                  </form>
              </b-modal>
            </div>
        </b-col>
      </b-row>
      </b-container>
    </div>
    <div id="body">
    <router-view :key="componentKey"></router-view><!--Most important thing. Used to display components-->
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
      return {
        user: {
          username: '',
          password: '',
          userId: '',
          mail: '',
          firstname:'',
          lastname:''
        },
        registerUser: {
          username: '',
          password: '',
          userId: '',
          mail: '',
          firstname:'',
          lastname:''
        },
        nameState: null,
        isConnected: false,
        search: '',
        componentKey: 0
      }
    },
    computed: {
      profile() {
        return this.$route.params.profile
      }
  },
    methods: {
      showModalSignIn() {
        this.$refs['modal-signin'].show()
      },
      showModalSignUp() {
        this.$refs['modal-signup'].show()
      },
      clearRegisterUserData() {
        this.registerUser = {
          username: '',
          password: '',
          userId: '',
          mail: '',
          firstname:'',
          lastname:''
        }
      },
      clearUserData() {
        this.user= {
          username: '',
          password: '',
          userId: '',
          mail: '',
          firstname:'',
          lastname:''
        }
      },
      forceRerender() {
        //console.log("Rerender")
        this.componentKey += 1
      },
      goHomePage()
      {
        try {
          this.$router.push('/')
        } catch (error) {
          //Only when already at root sooooo... https://gfycat.com/darlingmildguernseycow
        }
        this.forceRerender()
      },
      goToProfile()
      {
        console.log("Go to profile")
        this.$router.push('/profile/' + this.user.userId)
        try {
         
        } catch (error) {
          
        }
      },
      getSearch()
      {
        print(search)
      },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.nameState = valid
        return valid
      },
      resetModal() {
        this.user.username = ''
        this.nameState = null
      },
      handleOkIn(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault()
        // Trigger submit handler
        this.submitSignIn()
      },
      submitSignIn() {
        console.log("Submit Sign In !")
        if (!this.checkFormValidity()) {
          return
        }
        console.log("Username: " + this.user.username + " | Password: "+ this.user.password)
        this.logIn()
        this.$nextTick(() => {
          this.$refs['modal-signin'].hide()
        })
      },
      logIn() {
        var that = this
        var bodyFormData = new FormData()
        bodyFormData.append('username', this.user.username)
        bodyFormData.append('password', this.user.password)
        
        this.$refs['modal-loading'].show()

        this.$axios
          .post('http://127.0.0.1:5002/login', bodyFormData, {'Content-Type': 'multipart/form-data' })
          .then(res => {
            console.log(res)
            that.user = {
                          username: res.data.data.username,
                          password: '',
                          userId: res.data.data.id_user,
                          mail: res.data.data.email,
                          firstname: res.data.data.firstname,
                          lastname: res.data.data.lastname
                        }
            
            this.$bvToast.toast('You successfully signed in !', {
              title: 'Success !',
              autoHideDelay: 5000
            })
          })
          .catch(error =>{
            console.log(error)
            if(error.response.status === 406)
            {
              this.$bvToast.toast('Username or password is incorrect. Please try again.', {
                title: 'Wrong credentials',
                autoHideDelay: 15000
              })
            }
            else if(error.response.status === 401)
            {
              this.$bvToast.toast('Unlucky', {
                title: 'Session expired',
                autoHideDelay: 15000
              })
            }
            else
            {
              this.$bvToast.toast('Please contact stanislaw.karol.pluszkiewicz@gmail.com for any inconvenience.', {
                title: 'Somethin wrong happened.',
                autoHideDelay: 15000
              })
            }
          }).finally( f => {
              this.$refs['modal-loading'].hide()
              that.isConnected = true
          });
      },
      handleOkUp(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault()
        // Trigger submit handler
        this.submitSignUp()
      },
      submitSignUp() {
        console.log("Submit Sign Up !")
        this.signUp()
        this.$nextTick(() => {
          this.$refs['modal-signup'].hide()
        })
      },
      signUp() {
        var that = this
        var bodyFormData = new FormData()
        bodyFormData.append('username', this.registerUser.username)
        bodyFormData.append('password', this.registerUser.password)
        bodyFormData.append('email', this.registerUser.mail)
        bodyFormData.append('firstname', this.registerUser.firstname)
        bodyFormData.append('lastname', this.registerUser.lastname)
        
        this.$refs['modal-loading'].show()

        this.$axios
          .post('http://127.0.0.1:5002/register', bodyFormData, {'Content-Type': 'multipart/form-data' })
          .then(res => {
            console.log(res)
            this.$bvToast.toast('You successfully created your account. You can now sign in.', {
              title: 'Success !',
              autoHideDelay: 10000
            })
          })
          .catch(error =>{
            console.log(error)
              this.$bvToast.toast('Please contact stanislaw.karol.pluszkiewicz@gmail.com for any inconvenience.', {
                title: 'Somethin wrong happened.',
                autoHideDelay: 15000
              })
          }).finally( f => {
              this.$refs['modal-loading'].hide()
          });
      },
      logout() {
        this.clearUserData()
        this.clearRegisterUserData()
        this.isConnected = false
        document.cookie = 'token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
        this.$bvToast.toast('You logged out successfully !', {
                title: 'Success !',
                autoHideDelay: 15000
              })
      }
    }
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

#body {
    color: #000000;
    padding-top: 50px;
    padding-bottom: 15px;
    min-height: 100%;
    max-width: 80%;
    margin: 0 auto;
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
