<template>
  <div
    class="bg-cover flex h-screen justify-center items-center bg-gray-300"
    style="background-image: url(/static/images/siu9.jpg)"
  >
    <div class="shadow-xl mx-auto grid grid-cols-2 bg-white w-7/12">
      <div class="flex flex-col justify-center items-center">
        <img class="w-48 mb-8" src="/static/images/logo2.png" alt="Logo" />
        <div class="flex flex-col items-center w-3/5">
          <Input
            :icon="['fas', 'hashtag']"
            placeholder="Código o Correo Electrónico"
            :error="error"
            v-model="code.value"
          />
          <Input
            :icon="['fas', 'key']"
            :error="error"
            :message="message"
            placeholder="Contraseña"
            type="password"
            v-model="password.value"
          />

          <div class="mt-8 text-right w-full">
            <Button v-if="!loading" @click="onLogin($event)" fill>Iniciar Sesión</Button>
            <Spinner v-else />
            <br />
            <div class="mt-2">
              <Link to="/register" text="Crear Cuenta" />
              <span class="px-1">&bull;</span>
              <Link to="/forgot" text="Olvidaste tu contraseña?" />
            </div>
          </div>
        </div>
      </div>

      <div>
        <img class="h-140 w-full object-cover" src="/static/images/background.jpg" alt="Image" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Button from '@/components/public/Button.vue';
import { MUTATIONS as AuthMutations, ACTIONS as AuthActions } from '@/store/modules/auth';
import Input from '@/components/Input.vue';
import Link from '@/components/Link.vue';
import Spinner from '@/components/Spinner.vue';
import authService from '@/services/auth';

export default Vue.extend({
  components: {
    Button,
    Input,
    Spinner,
    Link,
  },
  data() {
    return {
      code: {
        value: '',
        error: '',
      },
      password: {
        value: '',
        error: '',
      },
      error: false,
      message: '',
      loading: false,
    };
  },
  methods: {
    async onLogin(e: Event): Promise<void> {
      e.preventDefault();
      this.message = '';
      this.error = false;
      this.loading = true;

      try {
        const response = await authService.login(this.code.value, this.password.value);
        this.$store.commit(AuthMutations.SET_TOKEN, response.data.token);
        this.$store.dispatch(AuthActions.FETCH_PROFILE);
      } catch (err) {
        this.message = err.response.data.message;
        this.error = true;
      } finally {
        this.loading = false;
        if (!this.error) {
          this.$router.push({ path: 'a' });
        }
      }
    },
  },
});
</script>
