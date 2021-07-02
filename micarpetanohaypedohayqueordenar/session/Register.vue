<template>
  <div
    class="bg-lcoal bg-cover flex h-screen justify-center items-center bg-black"
    style="background-image: url(/static/images/siu4.jpg)"
  >
    <div class="shadow-xl mx-auto grid grid-cols-2 bg-white w-7/12">
      <div>
        <img class="h-216 w-full object-cover" src="/static/images/background.jpg" alt="Image" />
      </div>

      <div class="flex flex-col justify-center items-center">
        <img class="w-48 mt-6" src="/static/images/logo2.png" alt="Logo" />
        <div class="flex flex-col items-center w-3/5 bg-white">
          <Input
            :icon="['fas', 'chalkboard-teacher']"
            type="text"
            placeholder="Código de estudiante"
            v-model="form.code.value"
            :error="form.code.errors.length > 0"
            :message="form.code.errors[0]"
          />
          <Input
            :icon="['fas', 'user-alt']"
            type="text"
            placeholder="Nombre(s)"
            v-model="form.name.value"
            :error="form.name.errors.length > 0"
            :message="form.name.errors[0]"
          />
          <Input
            :icon="['fas', 'user-alt']"
            type="text"
            placeholder="Apellido paterno"
            v-model="form.firstLastName.value"
            :error="form.firstLastName.errors.length > 0"
            :message="form.firstLastName.errors[0]"
          />
          <Input
            :icon="['fas', 'user-alt']"
            type="text"
            placeholder="Apellido materno"
            v-model="form.secondLastName.value"
            :error="form.secondLastName.errors.length > 0"
            :message="form.secondLastName.errors[0]"
          />
          <Input
            :icon="['fas', 'at']"
            type="text"
            placeholder="Correo electronico"
            v-model="form.email.value"
            :error="form.email.errors.length > 0"
            :message="form.email.errors[0]"
          />
          <Input
            :icon="['fas', 'key']"
            type="password"
            placeholder="Contraseña"
            v-model="form.password.value"
            :error="form.password.errors.length > 0"
            :message="form.password.errors[0]"
          />
          <Input
            :icon="['fas', 'lock']"
            type="password"
            placeholder="Verificar contraseña"
            v-model="form.verifyPassword.value"
            :error="form.verifyPassword.errors.length > 0"
            :message="form.verifyPassword.errors[0]"
          />
          <div class="mb-8 text-right w-full">
            <Button v-if="!loading" @click="register($event)" fill>Registrarse</Button>
            <Spinner v-else />
            <br />
            <Link text="Iniciar sesión" to="/login" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue';
import Button from '@/components/public/Button.vue';
import Spinner from '@/components/Spinner.vue';
import Input from '@/components/Input.vue';
import api from '@/services/auth';
import validation from '@/validator/registerValidation';
import { Field, PopperMessage } from '@/interfaces';
import { MUTATIONS as MessageMutations } from '@/store/modules/message';
import ID from '@/utils/generation';
import Link from '@/components/Link.vue';

export default Vue.extend({
  components: {
    Button,
    Input,
    Link,
    Spinner,
  },

  data() {
    return {
      form: {
        code: {
          value: '',
          errors: [],
        },
        name: {
          value: '',
          errors: [],
        },
        firstLastName: {
          value: '',
          errors: [],
        },
        secondLastName: {
          value: '',
          errors: [],
        },
        email: {
          value: '',
          errors: [],
        },
        password: {
          value: '',
          errors: [],
        },
        verifyPassword: {
          value: '',
          errors: [],
        },
      } as Record<string, Field>,
      loading: false,
    };
  },

  methods: {
    async register(e: Event): Promise<void> {
      e.preventDefault();
      this.loading = true;

      const { form } = this;

      Object.keys(form).forEach((key) => {
        this.form[key].errors = [];
      });

      const validated = validation(
        form.code.value,
        form.name.value,
        form.firstLastName.value,
        form.secondLastName.value,
        form.email.value,
        form.password.value,
        form.verifyPassword.value,
      );

      if (validated !== undefined) {
        Object.keys(validated).forEach((key) => {
          this.form[key].errors = validated[key];
        });
        this.loading = false;
        return;
      }
      try {
        const response = await api.register(
          form.code.value,
          form.name.value,
          form.firstLastName.value,
          form.secondLastName.value,
          form.email.value,
          form.password.value,
          form.verifyPassword.value,
        );

        const message = {
          level: 'success',
          title: 'Registro Exitoso',
          message:
            'Tu cuenta ha sido creada exitosamente. Se te ha enviado un correo para verificar tu cuenta',
          id: ID(),
          timeout: 8000,
        } as PopperMessage;

        this.$store.commit(MessageMutations.ADD_MESSAGE, message);
        this.$router.push({ path: '/login' });
      } catch (err) {
        Object.keys(err.response.data.errors).forEach((key) => {
          this.form[key].errors = err.response.data.errors[key];
        });
      } finally {
        this.loading = false;
      }
    },
  },
});
</script>
