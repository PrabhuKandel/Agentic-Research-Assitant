import type { Metadata } from "next";
import {Toaster} from "sonner"
import "./globals.css";

export const metadata: Metadata = {
  title: "Agentic Research Assistant",
  description: "Chat with your uploaded knowledge base.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}
            {/* Global toast container used by the whole application. */}
        <Toaster
          position="top-right"
          richColors
          closeButton
        />
        </body>
    </html>
  );
}
