<template>
  <div class="mb-6 w-full">
    <div class="flex flex-row shadow-sm w-full">
      <span :class="iconClass">
        <icon :icon="icon" />
      </span>
      <input
        :type="type"
        :placeholder="placeholder"
        :class="inputClass"
        ref="input"
        v-model="currentValue"
        :value="value"
      />
    </div>
    <span v-if="error && message.length > 0" :class="validationClass">{{ message }}</span>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: {
    icon: {
      type: [Object, Array, String],
      required: true,
    },
    type: {
      type: String,
      default: 'text',
    },
    value: {
      type: String,
      default: null,
    },
    placeholder: {
      type: String,
      default: '',
    },
    error: {
      type: Boolean,
      default: false,
    },
    warning: {
      type: Boolean,
      default: false,
    },
    message: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      currentValue: this.value,
      valueWhenFocus: null,
    };
  },
  computed: {
    inputClass(): Array<string> {
      const classes = [
        'py-2',
        'px-3',
        'w-full',
        'placeholder-gray-900',
        'border',
        'rounded-r-md',
      ];

      if (this.error) {
        classes.push('border-red-500');
      } else if (this.warning) {
        classes.push('border-orange-400');
      } else {
        classes.push('border-gray-300');
      }

      return classes;
    },
    iconClass(): Array<string> {
      const classes = [
        'w-10',
        'flex',
        'items-center',
        'justify-center',
        'text-white',
        'rounded-l-md',
      ];

      if (this.error) {
        classes.push('bg-red-600');
      } else if (this.warning) {
        classes.push('bg-orange-400');
      } else {
        classes.push('bg-gray-900');
      }

      return classes;
    },
    validationClass(): Array<string> {
      const classes = ['text-xs', 'pl-10'];

      if (this.error) {
        classes.push('text-red-600');
      } else if (this.warning) {
        classes.push('text-orange-400');
      }

      return classes;
    },
  },
  watch: {
    value(value) {
      this.currentValue = value;
    },
    currentValue(currentValue) {
      this.$emit('input', currentValue);
    },
  },
  methods: {
    onBlur(e: Event) {
      this.$emit('blur', e);
    },
  },
});
</script>
