const DragDropUpload = {
    template: `
        <section class="p-4">
            <h2 class="text-xl font-semibold mb-4">Drag & Drop Upload</h2>
            <div
                @click="triggerFileSelect"
                @dragover.prevent="handleDragOver"
                @dragleave="handleDragLeave"
                @drop.prevent="handleDrop"
                class="border-2 border-dashed border-gray-300 rounded-xl w-50 h-[250px]"
                :class="dropAreaClass"
            >
                <div class="flex justify-center items-center h-full cursor-pointer">Drag and drop your files here or click to select</div>
                <input type="file" multiple @change="handleFiles" ref="fileInput" class="hidden" />
            </div>
            <ul>
                <li v-for="file in files" :key="file.name">{{ file.name }} ({{ file.size }} bytes)</li>
            </ul>
            <div v-if="files.length > 0" class="mt-4">
                <button @click="uploadFiles" class="bg-blue-500 text-white px-4 py-2 rounded mr-2">Upload</button>
                <button @click="clearFiles" class="bg-red-500 text-white px-4 py-2 rounded">Clear</button>
            </div>
        </section>
    `,
    name: 'DragDropUpload',
    data() {
        return {
            files: [],
            isDragging: false,
        };
    },
    computed: {
        dropAreaClass() {
            return this.isDragging ? 'bg-blue-100' : 'bg-white';
        }
    },
    methods: {
        triggerFileSelect() {
            this.$refs.fileInput.click();
        },
        handleDrop(event) {
            this.isDragging = false;
            this.files = Array.from(event.dataTransfer.files);
        },
        handleDragOver(event) {
            this.isDragging = true;
        },
        handleDragLeave(event) {
            this.isDragging = false;
        },
        handleFiles(event) {
            this.files = Array.from(event.target.files);
        },
        uploadFiles() {
            // Implement actual upload logic here
            alert('Uploading files...');
        },
        clearFiles() {
            this.files = [];
        }
    }
};

