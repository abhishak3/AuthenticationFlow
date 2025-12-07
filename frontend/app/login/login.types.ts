export type LoginForm = {
  email: string;
  password: string;
}

export type Action = Partial<LoginForm>;