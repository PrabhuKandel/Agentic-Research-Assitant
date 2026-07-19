import ChatPageClient from "@/components/chat/ChatPageClient";

export default async function ChatPage({
  params,
}: {
  params: Promise<{ chatId: string }>;
}) {
  const { chatId } = await params;
  return <ChatPageClient chatId={chatId} />;
}
