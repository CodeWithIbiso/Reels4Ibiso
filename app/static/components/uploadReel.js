const UploadReel = {
    template: `
        <section class="p-4">
            <h2 class="text-xl font-semibold mb-4">Upload New Reel</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="reel in reels" :key="reel.id" class="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <img :src="reel.thumbnail" alt="Reel Thumbnail" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h3 class="text-lg font-bold">{{ reel.title }}</h3>
                        <p class="text-gray-600">{{ reel.description }}</p>
                        <button @click="viewDetails(reel)" class="mt-2 text-blue-500 hover:underline">View Details</button>
                    </div>
                </div>
            </div>
        </section>
    `,
    name: 'UploadReel',
    data() {
        return {
            reels: [
                { id: 1, title: 'Uploaded Reel 1', description: 'Description for Uploaded Reel 1', thumbnail: 'path/to/thumbnail1.jpg' },
                { id: 2, title: 'Uploaded Reel 2', description: 'Description for Uploaded Reel 2', thumbnail: 'path/to/thumbnail2.jpg' },
                // Add more reel objects as needed
            ]
        };
    },
    methods: {
        viewDetails(reel) {
            alert(`Viewing details for: ${reel.title}`);
            // Implement detailed view logic here
        } 
    }
};

const UploadReels = {
    template: `
        <section class="p-4">
            <h2 class="text-xl font-semibold mb-4">Uploaded Reels</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="reel in reels" :key="reel.id" class="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <img :src="reel.thumbnail" alt="Reel Thumbnail" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h3 class="text-lg font-bold">{{ reel.title }}</h3>
                        <p class="text-gray-600">{{ reel.description }}</p>
                        <button @click="viewDetails(reel)" class="mt-2 text-blue-500 hover:underline">View Details</button>
                    </div>
                </div>
            </div>
        </section>
    `,
    name: 'UploadedReels',
    data() {
        return {
            reels: [
                { id: 1, title: 'Uploaded Reel 1', description: 'Description for Uploaded Reel 1', thumbnail: 'path/to/thumbnail1.jpg' },
                { id: 2, title: 'Uploaded Reel 2', description: 'Description for Uploaded Reel 2', thumbnail: 'path/to/thumbnail2.jpg' },
                // Add more reel objects as needed
            ]
        };
    },
    methods: {
        viewDetails(reel) {
            alert(`Viewing details for: ${reel.title}`);
            // Implement detailed view logic here
        }
    }
};