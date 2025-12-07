'use client'

export default function Page() {
  return (
    <form className="w-[400px] flex flex-col gap-8 border rounded-xl p-4">
      <div className="flex gap-4">
        <label className="w-20" htmlFor="email">Email:</label>
        <input className="border rounded-sm grow h-10 p-2" type="email" id="email" />
      </div>
      <div className="flex gap-4">
        <label className="w-20" htmlFor="password">Password:</label>
        <input className="border rounded-sm grow h-10 p-2" type="password" id="password" />
      </div>
      <button className="bg-blue-500 p-1 cursor-pointer" type="button">Submit</button>
    </form>
  );
}