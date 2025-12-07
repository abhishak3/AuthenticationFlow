import { LoginForm } from "./login.types";

export function isFormValid(form: LoginForm) {
  if (
    form.email === "" 
    || form.password === ""
  ) {
    return false
  }

  return true;
}