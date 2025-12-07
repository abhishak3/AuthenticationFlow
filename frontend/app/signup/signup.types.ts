export type Status = 'loading' | 'success' | 'error' | null;

export type SignupForm = {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirm_password: string;
};