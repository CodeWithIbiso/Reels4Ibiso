const UploadedReels = {
    // <video :src="reel.url" controls class="w-full h-48"></video>
    template: `
        <section class="p-4">
            <h2 class="text-xl font-semibold mb-4">Uploaded Reels</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="reel in reels" :key="reel.id" class="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <a :href="reel.url" target="_blank">
                        <img :src="reel.thumbnail" alt="Reel" class="w-full h-96" />
                    </a>
                    <div class="p-4">
                        <h3 class="text-lg font-bold">{{ reel.title }}</h3>
                        <p class="text-gray-500">Created on: {{ new Date(reel.created_time).toLocaleDateString() }}</p>
                        <button @click="viewDetails(reel)" class="mt-2 text-blue-500 hover:underline">View Details</button>
                    </div>
                </div>
            </div>
        </section>
    `,
    name: 'UploadedReels',
    data() {
        return {
            reels: []
        };
    },
    methods: {
        viewDetails(reel) {
            alert(`Viewing details for: ${reel.title}`);
            // Implement detailed view logic here
        },
        async fetchReels() {
            try {
                const token = 'your-auth-token'; // Replace with actual token retrieval logic
                const response = await fetch('/reels', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.reels = await response.json(); 
            } catch (error) {
                console.error('Error fetching reels:', error);
            }
        }
    },
    created() {
        this.fetchReels();
    }
};