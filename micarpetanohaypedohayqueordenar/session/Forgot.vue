<template>
  <div
    class="bg-lcoal bg-cover flex h-screen justify-center items-center bg-black"
    style="background-image: url(/static/images/siu.jpg)"
  >
    <div class="shadow-xl mx-auto grid grid-cols-2 bg-white w-7/12">
      <div class="flex flex-col justify-center items-center">
        <img class="w-48" src="/static/images/logo2.png" alt="Logo" />
        <div class="flex flex-col items-center justify-center">
          <div class="w-3/5">
            <p class="text-center mb-4">
              Si olvidaste tu contraseña, escribe tu correo electronico para recuperarla
            </p>
            <Input
              :icon="['fas', 'at']"
              type="text"
              placeholder="Correo electronico"
              v-model="form.email.value"
              :error="form.email.errors.length > 0"
              :message="form.email.errors[0]"
            />
          </div>
        </div>
        <div>
          <router-link to="/login">
            <Button class="mr-2">Atras</Button>
          </router-link>
          <Button fill @click="forgot($event)">Enivar</Button>
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
import Input from '@/components/Input.vue';
import api from '@/services/auth';
import { MUTATIONS as MessageMutations } from '@/store/modules/message';
import { Field, PopperMessage } from '@/interfaces';
import ID from '@/utils/generation';
import validation from '@/validator/forgotValidation';

export default Vue.extend({
  data() {
    return {
      form: {
        email: {
          value: '',
          errors: [],
        },
      } as Record<string, Field>,
    };
  },
  components: {
    Button,
    Input,
  },
  methods: {
    async forgot(e: Event): Promise<void> {
      e.preventDefault();

      const { form } = this;

      this.form.email.errors = [];
      const validated = validation(form.email.value);

      if (validated !== undefined) {
        this.form.email.errors = validated.email;
        console.log('caca');
        return;
      }

      try {
        const response = await api.forgot(form.email.value);

        const message = {
          level: 'success',
          title: 'Correo Valido',
          message: 'Revisa tu correo electronico para cambiar tu contraseña',
          id: ID(),
          timeout: 8000,
        } as PopperMessage;

        this.$store.commit(MessageMutations.ADD_MESSAGE, message);
      } catch (err) {
        const message = {
          level: 'error',
          title: 'Correo invalido',
          message: 'No hemo podido encontrar tu correo, porfavor intena de nuevo',
          id: ID(),
          timeout: 8000,
        } as PopperMessage;

        this.$store.commit(MessageMutations.ADD_MESSAGE, message);
      }
    },
  },
});
</script>
