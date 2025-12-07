import { SignupForm } from "./signup.types";

export function isFormValid(form: SignupForm) {
  if (
    form.firstName === ""
    || form.lastName === ""
    || form.email === ""
    || form.password === ""
    || form.confirm_password === ""
    || form.password !== form.confirm_password
  ) {
    return false;
  }

  return true;
}