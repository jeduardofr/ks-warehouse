<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: {
    text: {
      type: String,
      default: '',
    },
    variant: {
      type: String,
      default: 'primary',
      validator(value: string) {
        return ['primary', 'secondary', 'danger', 'disable'].indexOf(value) !== -1;
      },
    },
    fill: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      base: {
        secondary: {
          color: 'gray-900',
          hover: 'gray-800',
        },
        danger: {
          color: 'red-500',
          hover: 'red-600',
        },
        disable: {
          color: 'gray-500',
          hover: 'gray-600',
        },
      },
      default: {
        color: 'blue-500',
        hover: 'blue-600',
      },
    };
  },
  computed: {
    currentClass(): Array<string> {
      const classes = [
        'border',
        'rounded',
        'py-2',
        'px-3',
        'text-sm',
        'font-bold',
        'focus:outline-none',
        'focus:shadow-outline',
      ];

      let variant = this.default;

      if (this.base[this.variant]) {
        variant = this.base[this.variant];
      }

      classes.push(`border-${variant.color}`);

      if (this.fill) {
        classes.push(`bg-${variant.color}`, 'text-white');
        classes.push(`hover:bg-${variant.hover}`);
      } else {
        classes.push(`text-${variant.hover}`);
      }

      return classes;
    },
    getAttributes() {
      return {
        disabled: this.disabled,
      };
    },
  },
  methods: {
    onBlur(e: Event) {
      this.$emit('blur', e);
    },
    onFocus(e: Event) {
      this.$emit('focus', e);
    },
    onClick(e: Event) {
      this.$emit('click', e);
    },
  },
  render(createElement) {
    return createElement(
      'button',
      {
        attrs: this.getAttributes,
        class: this.currentClass,
        on: {
          click: this.onClick,
          focus: this.onFocus,
          blur: this.onBlur,
        },
      },
      this.$slots.default,
    );
  },
});
</script>
