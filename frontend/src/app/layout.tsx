import type { Metadata } from "next";
import { Quicksand } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const quicksand = Quicksand({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "LearnOps",
  description: "LearnOps Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${quicksand.className} min-h-full`}>
        {children}
        <Toaster
          position="top-center"
          classNames={{
            toast: "rounded-2xl shadow-lg w-[380px]",
          }}
        />
      </body>
    </html>
  );
}