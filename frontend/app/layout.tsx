import type { Metadata } from "next";
import {  Roboto } from "next/font/google";
import "./globals.css";

const roboto = Roboto({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "User Auth Flow",
  description: "Designing a JWT Auth Flow"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${roboto.className} antialiased w-screen h-screen flex justify-center items-center`}
      >
        {children}
      </body>
    </html>
  );
}
