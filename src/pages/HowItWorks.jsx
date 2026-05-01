export default function HowItWorks() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-10">
      <h2 className="text-2xl font-bold text-center mb-8">How SilentSOS Works</h2>
      
      <div className="space-y-4">
        <div className="bg-gray-900 rounded-xl p-6">
          <h3 className="font-bold text-red-400 mb-2">1. You type a message</h3>
          <p className="text-gray-400">Type what you want to say - looks completely normal</p>
        </div>
        
        <div className="bg-gray-900 rounded-xl p-6">
          <h3 className="font-bold text-red-400 mb-2">2. AI analyzes for hidden distress</h3>
          <p className="text-gray-400">Detects reassurance patterns, coercion cues, and unusual phrasing</p>
        </div>
        
        <div className="bg-gray-900 rounded-xl p-6">
          <h3 className="font-bold text-red-400 mb-2">3. Silent alert triggers if needed</h3>
          <p className="text-gray-400">Trusted contacts receive SMS with your location and risk level</p>
        </div>
        
        <div className="bg-gray-900 rounded-xl p-6">
          <h3 className="font-bold text-red-400 mb-2">4. You stay completely invisible</h3>
          <p className="text-gray-400">No panic button, no visible action - just protection</p>
        </div>
      </div>
    </div>
  )
}