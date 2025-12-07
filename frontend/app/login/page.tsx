'use client'

import { useReducer, useState } from "react";
import Link from "next/link";

import { isFormValid } from "./login.helper";
import { Action, LoginForm } from "./login.types";

import { Status } from "../signup/signup.types";

export default function Page() {
  const initialState: LoginForm = {
    email: "",
    password: ""
  }

  function reducer(state: LoginForm, action: Action) {
    return {
      ...state,
      ...action
    }
  }

  const [form, dispatch] = useReducer(reducer, initialState);
  const [status, setStatus] = useState<Status>(null);

  function onFormSubmit() {
    if (!isFormValid(form)) {
      setStatus('error');
      return;
    }

    const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

    setStatus('loading');

    fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: form.email,
        password: form.password
      }),
    })
    .then(() => {
      setStatus('success');
      dispatch(initialState);
    })
    .catch(() => setStatus('error'));
  }

  return (
    <div className="flex flex-col gap-4">
      <form className="w-[400px] flex flex-col gap-8 border rounded-xl p-4">
        <div className="flex gap-4">
          <label className="w-20" htmlFor="email">Email:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="email"
            id="email"
            value={form.email}
            onChange={(e) => dispatch({email: e.target.value})}
          />
        </div>
        <div className="flex gap-4">
          <label className="w-20" htmlFor="password">Password:</label>
          <input
            className="border rounded-sm grow h-10 p-2"
            type="password"
            id="password"
            value={form.password}
            onChange={(e) => dispatch({password: e.target.value})}
          />
        </div>
        <button
          className="bg-blue-500 p-1 cursor-pointer"
          type="button"
          onClick={onFormSubmit}>
            Submit
        </button>
        {status === 'error' && <span className="text-red-400">Form is not valid!</span>}
      </form>
      <span>New User? <Link className="text-blue-400" href="/signup">Sign Up</Link></span>
    </div>
  );
}