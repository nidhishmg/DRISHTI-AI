"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"; // Note: Need input component, will assume or mock it here if not created. I'll stick to standard input first or create ui/input
import { Send, Mic, Paperclip } from "lucide-react";
import { cn } from "@/lib/utils";

// Simple Input component since I didn't create one
function SimpleInput({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
    return (
        <input
            className={cn(
                "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                className
            )}
            {...props}
        />
    )
}

export default function DemoPage() {
    const [messages, setMessages] = useState([
        { role: "ai", text: "Namaste! I am Drushti Sahayak. You can report issues with government schemes here. You can type or send a voice note." }
    ]);
    const [input, setInput] = useState("");

    const handleSend = () => {
        if (!input.trim()) return;
        setMessages(prev => [...prev, { role: "user", text: input }]);
        setInput("");

        // Simulate AI response
        setTimeout(() => {
            setMessages(prev => [...prev, { role: "ai", text: "I have received your complaint. Analyzing it against existing clusters..." }]);
        }, 1000);
    };

    const handleVoice = () => {
        setMessages(prev => [...prev, { role: "user", text: "🎤 [Voice Note Uploaded] (0:45s)" }]);
        setTimeout(() => {
            setMessages(prev => [...prev, { role: "ai", text: "Transcribing voice note... I understood: 'My pension has not arrived for 3 months due to server link failure at the bank.' Is this correct?" }]);
        }, 1500);
    };

    return (
        <div className="flex h-[calc(100vh-6rem)] items-center justify-center">
            <div className="w-full max-w-md overflow-hidden rounded-xl border border-white/10 bg-black shadow-2xl">
                <div className="bg-[#075E54] p-4 flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-white/20" />
                    <div>
                        <h3 className="text-white font-bold">Drushti AI</h3>
                        <p className="text-xs text-white/80">Online</p>
                    </div>
                </div>

                <div className="h-[500px] bg-[url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')] bg-repeat p-4 space-y-4 overflow-y-auto">
                    {messages.map((msg, i) => (
                        <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[80%] rounded-lg p-3 text-sm shadow-sm ${msg.role === 'user' ? 'bg-[#DCF8C6] text-black' : 'bg-white text-black'}`}>
                                {msg.text}
                                <div className="mt-1 text-[10px] text-gray-500 text-right">
                                    {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="bg-[#f0f0f0] p-3 flex gap-2 items-center">
                    <Button variant="ghost" size="icon" className="text-gray-500"><Mic onClick={handleVoice} /></Button>
                    <SimpleInput
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a message..."
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        className="border-none bg-white rounded-full px-4 h-10"
                    />
                    <Button size="icon" className="bg-[#075E54] hover:bg-[#128C7E] rounded-full h-10 w-10" onClick={handleSend}>
                        <Send className="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
