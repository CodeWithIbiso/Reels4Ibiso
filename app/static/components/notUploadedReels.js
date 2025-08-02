const NotUploadedReels = {
    template: `
        <section class="p-4">
            <h2 class="text-xl font-semibold mb-4">Not Uploaded Reels</h2>
            <div class="mb-4">
                <button @click="activeTab = 'videos'" :class="{'font-bold': activeTab === 'videos'}" class="mr-4">Videos</button>
                <button @click="activeTab = 'photos'" :class="{'font-bold': activeTab === 'photos'}">Photos</button>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="file in filteredFiles" :key="file.id" class="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <img v-if="isImage(file.content_type)" :src="file.url" alt="File Thumbnail" class="w-full h-48 object-cover">
                    <video v-else-if="isVideo(file.content_type)" :src="file.url" :title="file.name" @click="showVideoModal(file)" class="w-full h-48 object-cover cursor-pointer"></video>
                    <div class="p-4">
                        <h3 class="text-lg font-bold">{{ file.name }}</h3>
                        <button @click="uploadFile(file)" class="mt-2 text-blue-500 hover:underline">Upload</button>
                        <button @click="removeFile(file)" class="mt-2 text-red-500 hover:underline ml-2">Remove</button>
                        <button @click="selectFile(file)" class="mt-2 text-green-500 hover:underline ml-2">Select</button>
                    </div>
                </div>
            </div>

            <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
                <div class="bg-white rounded-lg overflow-hidden">
                    <div class="flex justify-end p-2">
                        <button @click="closeVideoModal" class="text-gray-700 hover:text-gray-900">&times;</button>
                    </div>
                    <video :src="currentVideo.url" controls class="w-full h-64"></video>
                    <div class="p-4">
                        <h3 class="text-xl font-semibold">{{ currentVideo.name }}</h3>
                    </div>
                </div>
            </div>
        </section>
    `,
    name: 'NotUploadedReels',
    data() {
        return {
            files: [],
            showModal: false,
            currentVideo: null,
            activeTab: 'videos',
            selectedFiles: []
        };
    },
    computed: {
        filteredFiles() {
            return this.files.filter(file => 
                (this.activeTab === 'videos' && this.isVideo(file.content_type)) ||
                (this.activeTab === 'photos' && this.isImage(file.content_type))
            );
        }
    },
    methods: {
        uploadFile(file) {
            alert(`Uploading: ${file.name}`);
        },
        async fetchUploadedFiles() {
            try {
                const response = await fetch('/api/uploaded-files/');
                const data = await response.json();
                this.files = data.files;
            } catch (error) {
                console.error('Error fetching uploaded files:', error);
            }
        },
        isImage(contentType) {
            return contentType.startsWith('image/');
        },
        isVideo(contentType) {
            return contentType.startsWith('video/');
        },
        showVideoModal(file) {
            this.currentVideo = file;
            this.showModal = true;
        },
        closeVideoModal() {
            this.showModal = false;
            this.currentVideo = null;
        },
        async removeFile(file) {
            try {
                const response = await fetch(`/api/files/${file.id}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
            this.files = this.files.filter(f => f.id !== file.id);
                    alert('File removed successfully');
            } else {
                    const errorData = await response.json();
                    alert(`Error removing file: ${errorData.detail}`);
            }
            } catch (error) {
                console.error('Error removing file:', error);
                alert('An error occurred while removing the file.');
            }
        },
        selectFile(file) {
            if (this.selectedFiles.includes(file)) {
                this.selectedFiles = this.selectedFiles.filter(f => f.id !== file.id);
            } else {
                this.selectedFiles.push(file);
            }
            if (this.selectedFiles.length === 2) {
                this.processSelectedFiles();
            }
        },
        processSelectedFiles() {
            alert(`Processing files: ${this.selectedFiles.map(f => f.name).join(' and ')}`);
            this.selectedFiles = [];
        }
    },
    created() {
        this.fetchUploadedFiles();
    }
};